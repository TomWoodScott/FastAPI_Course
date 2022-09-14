from fastapi import APIRouter, status, HTTPException, Depends
from ..import schemas, database, models
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Users'],
    prefix="/user")

get_db = database.get_db



@router.post('/')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}')
def delete_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user