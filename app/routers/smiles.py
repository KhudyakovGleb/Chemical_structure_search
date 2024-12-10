from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.smile import Smile
from app.structure_search import substructure_search

router = APIRouter()


class SmileOut(BaseModel):
    id: str
    component: str

    class Config:
        from_attributes = True


class SmileCreate(BaseModel):
    id: str
    component: str


@router.get("/", response_model=list[SmileOut])
async def list_smiles(db: Session = Depends(get_db)) -> list[Smile]:
    return db.query(Smile).all()


@router.get("/{id}", response_model=SmileOut)
async def get_smile(id: str, db: Session = Depends(get_db)) -> Smile:
    smile = db.query(Smile).filter(Smile.id == id).first()
    if not smile:
        raise HTTPException(status_code=404, detail="Not found")
    return smile


@router.get("/search/", response_model=list[str])
async def get_search_for_smile(
    substructure: str, db: Session = Depends(get_db)
) -> list:
    components = [smile.component for smile in db.query(Smile).all()]
    return substructure_search(components, substructure)


@router.post("/", response_model=SmileOut)
async def create_smile(smile: SmileCreate, db: Session = Depends(get_db)) -> Smile:
    existing_smile = db.query(Smile).filter(Smile.id == smile.id).first()
    if existing_smile:
        raise HTTPException(status_code=400, detail="Smile with this ID already exists")

    new_smile = Smile(id=smile.id, component=smile.component)
    db.add(new_smile)
    db.commit()
    db.refresh(new_smile)
    return new_smile


@router.put("/{id}", response_model=SmileOut)
async def update_smile(
    id: str, new_smile: SmileCreate, db: Session = Depends(get_db)
) -> Smile:
    smile = db.query(Smile).filter(Smile.id == id).first()
    if not smile:
        raise HTTPException(status_code=404, detail="Not found")
    smile.component = new_smile.component
    db.commit()
    db.refresh(smile)
    return smile


@router.delete("/{id}", response_model=SmileOut)
async def delete_smile(id: str, db: Session = Depends(get_db)) -> Smile:
    smile = db.query(Smile).filter(Smile.id == id).first()
    if not smile:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(smile)
    db.commit()
    return smile
