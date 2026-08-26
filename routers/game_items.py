from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import get_db

router = APIRouter(
    prefix="/api/v1/game_items",
    tags=["game_items"],
)

def create_crud_endpoints(router, model_class, schema_class, schema_create_class, path_name):
    @router.get(f"/{path_name}/", response_model=List[schema_class])
    def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        items = db.query(model_class).offset(skip).limit(limit).all()
        return items

create_crud_endpoints(router, models.GdRockAsset, schemas.GdRockAsset, schemas.GdRockAssetCreate, "rock_assets")
create_crud_endpoints(router, models.GdRock, schemas.GdRock, schemas.GdRockCreate, "rocks")
create_crud_endpoints(router, models.GdBroomAsset, schemas.GdBroomAsset, schemas.GdBroomAssetCreate, "broom_assets")
create_crud_endpoints(router, models.GdBroom, schemas.GdBroom, schemas.GdBroomCreate, "brooms")
create_crud_endpoints(router, models.GdRockPusherAsset, schemas.GdRockPusherAsset, schemas.GdRockPusherAssetCreate, "rock_pusher_assets")
create_crud_endpoints(router, models.GdRockPusher, schemas.GdRockPusher, schemas.GdRockPusherCreate, "rock_pushers")
create_crud_endpoints(router, models.GdSurfaceMaterial, schemas.GdSurfaceMaterial, schemas.GdSurfaceMaterialCreate, "surface_materials")
create_crud_endpoints(router, models.GdSurface, schemas.GdSurface, schemas.GdSurfaceCreate, "surfaces")
create_crud_endpoints(router, models.GdGameCurrency, schemas.GdGameCurrency, schemas.GdGameCurrencyCreate, "currencies")
