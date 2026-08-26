from fastapi import APIRouter, Depends, HTTPException, Query, Request, Body
from sqlalchemy.orm import Session
import inspect
from typing import Any, Dict, List, Union
from database import get_db
import models

router = APIRouter(prefix="/rest/v1", tags=["GameData"])

# Map table names to SQLAlchemy models
TABLE_MAP = {}
for name, obj in inspect.getmembers(models, inspect.isclass):
    if hasattr(obj, '__tablename__'):
        TABLE_MAP[obj.__tablename__] = obj

def serialize_model(instance) -> dict:
    d = {k: v for k, v in instance.__dict__.items() if not k.startswith('_')}
    for k, v in list(d.items()):
        if hasattr(v, 'isoformat'):
            d[k] = v.isoformat()
    return d

def apply_query_filters(query, model_cls, params: dict):
    for key, value in params.items():
        if key in ('select', 'order', 'limit', 'offset', 'apikey'):
            continue
        if not hasattr(model_cls, key):
            continue
        
        column = getattr(model_cls, key)
        if isinstance(value, str):
            if value.startswith('eq.'):
                val = value[3:]
                if val.lower() == 'true': val = True
                elif val.lower() == 'false': val = False
                elif val.lower() == 'null': val = None
                query = query.filter(column == val)
            elif value.startswith('neq.'):
                val = value[4:]
                if val.lower() == 'true': val = True
                elif val.lower() == 'false': val = False
                elif val.lower() == 'null': val = None
                query = query.filter(column != val)
            elif value.startswith('gt.'):
                query = query.filter(column > value[3:])
            elif value.startswith('gte.'):
                query = query.filter(column >= value[4:])
            elif value.startswith('lt.'):
                query = query.filter(column < value[3:])
            elif value.startswith('lte.'):
                query = query.filter(column <= value[4:])
            elif value.startswith('like.'):
                query = query.filter(column.like(value[5:]))
            elif value.startswith('ilike.'):
                query = query.filter(column.ilike(value[6:]))
            elif value.startswith('in.(') and value.endswith(')'):
                items = [x.strip() for x in value[4:-1].split(',')]
                query = query.filter(column.in_(items))
            else:
                query = query.filter(column == value)
        else:
            query = query.filter(column == value)
            
    order = params.get('order')
    if order and hasattr(model_cls, order.split('.')[0]):
        col_name = order.split('.')[0]
        direction = order.split('.')[1] if '.' in order else 'asc'
        col = getattr(model_cls, col_name)
        query = query.order_by(col.desc() if direction == 'desc' else col.asc())
    elif hasattr(model_cls, 'id'):
        query = query.order_by(model_cls.id.asc())

    if 'limit' in params and params['limit'].isdigit():
        query = query.limit(int(params['limit']))
    if 'offset' in params and params['offset'].isdigit():
        query = query.offset(int(params['offset']))

    return query

import re
from sqlalchemy import text

@router.get("/{table_name}")
def get_table_data(
    table_name: str, 
    request: Request,
    db: Session = Depends(get_db)
):
    if not re.match(r'^[a-zA-Z0-9_]+$', table_name):
        raise HTTPException(status_code=400, detail="Invalid table name")

    try:
        params = dict(request.query_params)
        where_clauses = []
        sql_params = {}
        
        param_idx = 0
        for key, value in params.items():
            if key in ('select', 'order', 'limit', 'offset', 'apikey'):
                continue
            if not re.match(r'^[a-zA-Z0-9_]+$', key):
                continue
                
            param_idx += 1
            param_key = f"p_{key}_{param_idx}"
            if isinstance(value, str):
                if value.startswith('eq.'):
                    val = value[3:]
                    if val.lower() == 'null':
                        where_clauses.append(f"`{key}` IS NULL")
                    elif val.lower() == 'true':
                        where_clauses.append(f"`{key}` = 1")
                    elif val.lower() == 'false':
                        where_clauses.append(f"`{key}` = 0")
                    else:
                        where_clauses.append(f"`{key}` = :{param_key}")
                        sql_params[param_key] = val
                elif value.startswith('neq.'):
                    val = value[4:]
                    if val.lower() == 'null':
                        where_clauses.append(f"`{key}` IS NOT NULL")
                    elif val.lower() == 'true':
                        where_clauses.append(f"`{key}` != 1")
                    elif val.lower() == 'false':
                        where_clauses.append(f"`{key}` != 0")
                    else:
                        where_clauses.append(f"`{key}` != :{param_key}")
                        sql_params[param_key] = val
                elif value.startswith('gt.'):
                    where_clauses.append(f"`{key}` > :{param_key}")
                    sql_params[param_key] = value[3:]
                elif value.startswith('gte.'):
                    where_clauses.append(f"`{key}` >= :{param_key}")
                    sql_params[param_key] = value[4:]
                elif value.startswith('lt.'):
                    where_clauses.append(f"`{key}` < :{param_key}")
                    sql_params[param_key] = value[3:]
                elif value.startswith('lte.'):
                    where_clauses.append(f"`{key}` <= :{param_key}")
                    sql_params[param_key] = value[4:]
                elif value.startswith('like.'):
                    where_clauses.append(f"`{key}` LIKE :{param_key}")
                    sql_params[param_key] = value[5:]
                elif value.startswith('ilike.'):
                    where_clauses.append(f"`{key}` LIKE :{param_key}")
                    sql_params[param_key] = value[6:]
                elif value.startswith('in.(') and value.endswith(')'):
                    items = [x.strip() for x in value[4:-1].split(',')]
                    in_placeholders = []
                    for i, item in enumerate(items):
                        pk = f"{param_key}_{i}"
                        in_placeholders.append(f":{pk}")
                        sql_params[pk] = item
                    where_clauses.append(f"`{key}` IN ({', '.join(in_placeholders)})")
                else:
                    where_clauses.append(f"`{key}` = :{param_key}")
                    sql_params[param_key] = value
            else:
                where_clauses.append(f"`{key}` = :{param_key}")
                sql_params[param_key] = value

        select_cols = "*"
        if 'select' in params and params['select']:
            cols = [c.strip() for c in params['select'].split(',') if re.match(r'^[a-zA-Z0-9_]+$', c.strip())]
            if cols:
                select_cols = ", ".join([f"`{c}`" for c in cols])

        sql = f"SELECT {select_cols} FROM `{table_name}`"
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
            
        order = params.get('order')
        if order:
            parts = order.split('.')
            col_name = parts[0]
            if re.match(r'^[a-zA-Z0-9_]+$', col_name):
                direction = 'DESC' if len(parts) > 1 and parts[1].lower() == 'desc' else 'ASC'
                sql += f" ORDER BY `{col_name}` {direction}"
        else:
            # Check if id column exists for default sort
            sql += " ORDER BY `id` ASC"

        if 'limit' in params and params['limit'].isdigit():
            sql += f" LIMIT {int(params['limit'])}"
        if 'offset' in params and params['offset'].isdigit():
            sql += f" OFFSET {int(params['offset'])}"

        result = db.execute(text(sql), sql_params)
        columns = result.keys()
        rows = result.fetchall()
        
        output = []
        for row in rows:
            row_dict = {}
            for col, val in zip(columns, row):
                if hasattr(val, 'isoformat'):
                    row_dict[col] = val.isoformat()
                elif isinstance(val, (bytes, bytearray)):
                    row_dict[col] = bool(val[0])
                else:
                    row_dict[col] = val
            output.append(row_dict)
            
        return output
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{table_name}")
def create_table_data(
    table_name: str,
    payload: Union[Dict[str, Any], List[Dict[str, Any]]] = Body(...),
    db: Session = Depends(get_db)
):
    model_cls = TABLE_MAP.get(table_name)
    if not model_cls:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
    items = payload if isinstance(payload, list) else [payload]
    created = []
    
    try:
        for item in items:
            valid_cols = {c.name for c in model_cls.__table__.columns}
            clean_item = {}
            for k, v in item.items():
                if k not in valid_cols:
                    continue
                col_type = type(model_cls.__table__.columns[k].type).__name__
                if col_type in ("DateTime", "TIMESTAMP") and isinstance(v, str) and v:
                    try:
                        import datetime
                        clean_item[k] = datetime.datetime.fromisoformat(v.replace("Z", "+00:00")).replace(tzinfo=None)
                    except Exception:
                        clean_item[k] = None
                else:
                    clean_item[k] = v
            
            if table_name == "ud_user_master" and "id" not in clean_item:
                import random
                while True:
                    candidate_id = random.randint(100_000_000, 999_999_999)
                    if not db.query(models.UdUserMaster).filter(models.UdUserMaster.id == candidate_id).first():
                        clean_item["id"] = candidate_id
                        break

            record = model_cls(**clean_item)
            db.add(record)
            db.flush()
            db.refresh(record)
            created.append(serialize_model(record))
            
        db.commit()
        # PostgREST always returns an array of records
        return created
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{table_name}")
def update_table_data(
    table_name: str,
    request: Request,
    payload: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    model_cls = TABLE_MAP.get(table_name)
    if not model_cls:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
    try:
        query = db.query(model_cls)
        query = apply_query_filters(query, model_cls, dict(request.query_params))
        records = query.all()
        
        if not records:
            return []
        
        valid_cols = {c.name for c in model_cls.__table__.columns}
        clean_payload = {}
        for k, v in payload.items():
            if k not in valid_cols:
                continue
            col_type = type(model_cls.__table__.columns[k].type).__name__
            if col_type in ("DateTime", "TIMESTAMP") and isinstance(v, str) and v:
                try:
                    import datetime
                    clean_payload[k] = datetime.datetime.fromisoformat(v.replace("Z", "+00:00")).replace(tzinfo=None)
                except Exception:
                    clean_payload[k] = None
            else:
                clean_payload[k] = v
        
        updated = []
        for r in records:
            for k, v in clean_payload.items():
                setattr(r, k, v)
            db.flush()
            db.refresh(r)
            updated.append(serialize_model(r))
            
        db.commit()
        return updated
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{table_name}")
def delete_table_data(
    table_name: str,
    request: Request,
    db: Session = Depends(get_db)
):
    model_cls = TABLE_MAP.get(table_name)
    if not model_cls:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
    try:
        query = db.query(model_cls)
        query = apply_query_filters(query, model_cls, dict(request.query_params))
        records = query.all()
        
        for r in records:
            db.delete(r)
        db.commit()
        return {"deleted": len(records)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/rpc/{function_name}")
def execute_rpc(
    function_name: str,
    payload: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    try:
        if function_name == "record_daily_activity":
            record = models.AnalysisUserDailyActivity(
                p_user_id=payload.get("p_user_id"),
                p_platform=payload.get("p_platform", "Android"),
                p_app_version=payload.get("p_app_version", "1.0.0"),
            )
            db.add(record)
            db.commit()
            return {"status": "ok"}
        
        # Generic RPC handler for other analytics functions
        return {"status": "ok", "function": function_name}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

