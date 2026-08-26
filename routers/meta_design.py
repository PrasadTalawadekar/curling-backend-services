from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/api/v1/meta-design",
    tags=["Meta Design"]
)

def crud_helper(router, model, schema_create, schema_update, schema_response, path):
    @router.get(f"{path}", response_model=List[schema_response])
    def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return db.query(model).offset(skip).limit(limit).all()

    @router.post(f"{path}", response_model=schema_response)
    def create_item(item: schema_create, db: Session = Depends(get_db)):
        db_item = model(**item.model_dump(exclude_unset=True))
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @router.get(f"{path}/{{item_id}}", response_model=schema_response)
    def read_item(item_id: int, db: Session = Depends(get_db)):
        db_item = db.query(model).filter(model.id == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

    @router.put(f"{path}/{{item_id}}", response_model=schema_response)
    def update_item(item_id: int, item: schema_update, db: Session = Depends(get_db)):
        db_item = db.query(model).filter(model.id == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in item.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item

    @router.delete(f"{path}/{{item_id}}")
    def delete_item(item_id: int, db: Session = Depends(get_db)):
        db_item = db.query(model).filter(model.id == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(db_item)
        db.commit()
        return {"ok": True}

crud_helper(router, models.GdFeature, schemas.GdFeatureCreate, schemas.GdFeatureUpdate, schemas.GdFeature, "/features")
crud_helper(router, models.GdWidget, schemas.GdWidgetCreate, schemas.GdWidgetUpdate, schemas.GdWidget, "/widgets")
crud_helper(router, models.GdGameScreen, schemas.GdGameScreenCreate, schemas.GdGameScreenUpdate, schemas.GdGameScreen, "/screens")
crud_helper(router, models.GdGameScreenWidgetFeatureMapper, schemas.GdGameScreenWidgetFeatureMapperCreate, schemas.GdGameScreenWidgetFeatureMapperUpdate, schemas.GdGameScreenWidgetFeatureMapper, "/game-screen-widget-feature-mappers")
crud_helper(router, models.GdGameflowConfig, schemas.GdGameflowConfigCreate, schemas.GdGameflowConfigUpdate, schemas.GdGameflowConfig, "/gameflow-configs")
crud_helper(router, models.GdGameflow, schemas.GdGameflowCreate, schemas.GdGameflowUpdate, schemas.GdGameflow, "/gameflows")
crud_helper(router, models.GdChallenge, schemas.GdChallengeCreate, schemas.GdChallengeBase, schemas.GdChallenge, "/feature-challenges")
crud_helper(router, models.GdChallengeConfig, schemas.GdChallengeConfigCreate, schemas.GdChallengeConfigBase, schemas.GdChallengeConfig, "/feature-challenge-configs")
crud_helper(router, models.GdScenario, schemas.GdScenarioCreate, schemas.GdScenarioBase, schemas.GdScenario, "/scenarios")

# --- GdEnvironmentAsset ---
@router.get("/environment-assets/", response_model=List[schemas.GdEnvironmentAsset])
def read_environment_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.GdEnvironmentAsset).offset(skip).limit(limit).all()
@router.get("/environment-assets/{asset_id}", response_model=schemas.GdEnvironmentAsset)
def read_environment_asset(asset_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.GdEnvironmentAsset).filter(models.GdEnvironmentAsset.id == asset_id).first()
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Environment Asset not found")
    return db_obj

# --- GdEnvironment ---
@router.get("/environments/", response_model=List[schemas.GdEnvironment])
def read_environments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.GdEnvironment).offset(skip).limit(limit).all()

@router.get("/environments/{environment_id}", response_model=schemas.GdEnvironment)
def read_environment(environment_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.GdEnvironment).filter(models.GdEnvironment.id == environment_id).first()
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Environment not found")
    return db_obj
