from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import inspect
from database import get_db
import models

router = APIRouter(prefix="/rest/v1", tags=["GameData"])

# Map table names to SQLAlchemy models
TABLE_MAP = {}
for name, obj in inspect.getmembers(models, inspect.isclass):
    if hasattr(obj, '__tablename__'):
        TABLE_MAP[obj.__tablename__] = obj

@router.get("/{table_name}")
def get_table_data(
    table_name: str, 
    select: str = Query(None),
    order: str = Query(None),
    db: Session = Depends(get_db)
):
    model_cls = TABLE_MAP.get(table_name)
    if not model_cls:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
    query = db.query(model_cls)
    if hasattr(model_cls, 'id'):
        query = query.order_by(model_cls.id.asc())
        
    records = query.all()
    result = []
    for r in records:
        d = {k: v for k, v in r.__dict__.items() if not k.startswith('_')}
        for k, v in list(d.items()):
            if hasattr(v, 'isoformat'):
                d[k] = v.isoformat()
        result.append(d)
    return result
