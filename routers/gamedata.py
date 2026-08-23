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

@router.get("/{table_name}")
def get_table_data(
    table_name: str, 
    request: Request,
    db: Session = Depends(get_db)
):
    model_cls = TABLE_MAP.get(table_name)
    if not model_cls:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
    query = db.query(model_cls)
    query = apply_query_filters(query, model_cls, dict(request.query_params))
    records = query.all()
    return [serialize_model(r) for r in records]

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
    
    for item in items:
        valid_cols = {c.name for c in model_cls.__table__.columns}
        clean_item = {k: v for k, v in item.items() if k in valid_cols}
        
        record = model_cls(**clean_item)
        db.add(record)
        db.flush()
        db.refresh(record)
        created.append(serialize_model(record))
        
    db.commit()
    return created if isinstance(payload, list) else (created[0] if created else {})

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
    
    query = db.query(model_cls)
    query = apply_query_filters(query, model_cls, dict(request.query_params))
    records = query.all()
    
    if not records:
        return []
    
    valid_cols = {c.name for c in model_cls.__table__.columns}
    clean_payload = {k: v for k, v in payload.items() if k in valid_cols}
    
    updated = []
    for r in records:
        for k, v in clean_payload.items():
            setattr(r, k, v)
        db.flush()
        db.refresh(r)
        updated.append(serialize_model(r))
        
    db.commit()
    return updated

@router.delete("/{table_name}")
def delete_table_data(
    table_name: str,
    request: Request,
    db: Session = Depends(get_db)
):
    model_cls = TABLE_MAP.get(table_name)
    if not model_cls:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
    query = db.query(model_cls)
    query = apply_query_filters(query, model_cls, dict(request.query_params))
    records = query.all()
    
    for r in records:
        db.delete(r)
    db.commit()
    return {"deleted": len(records)}
