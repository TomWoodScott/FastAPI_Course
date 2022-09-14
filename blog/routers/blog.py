from fastapi import APIRouter, status, HTTPException, Depends
from ..import schemas, database, models
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()

get_db = database.get_db

# Return all blogs,
@router.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=["blogs"])
def show_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No blogs currently exist")
    return blogs


# Create blog
@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(request:schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Return blog by id
@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["blogs"])
def show_by_id(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                    detail = f"blog with id {id} does not exist")
    return blog

# Delete blog by id
@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def delete(id, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return {'response' : 'Blog with id {id} deleted'}


# Update blog by id
@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found")

    blog.update(request)
    db.commit()
    return 'Updated successfully'