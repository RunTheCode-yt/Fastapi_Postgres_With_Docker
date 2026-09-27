import uuid

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import ItemCreate, ItemResponse
from models import Base, ModelItem
from database import engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):

    db_item = ModelItem(title=item.title, description=item.description)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


@app.get("/items", response_model=list[ItemResponse])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    db_items = db.query(ModelItem).offset(skip).limit(limit).all()
    return db_items


@app.get("/item/{item_id}", response_model=ItemResponse)
def get_item(item_id:uuid.UUID, db: Session = Depends(get_db)):

    db_item = db.query(ModelItem).filter(ModelItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
