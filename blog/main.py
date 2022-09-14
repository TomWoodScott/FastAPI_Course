from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a blog, add it to the database
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Return all blogs,  
@app.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def show_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"No blogs currently exist")
    return blogs


# Return blog by id
@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show_by_id(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                    detail = f"blog with id {id} does not exist")
#        response.status_code = status.HTTP_404_NOT_FOUND
#        return {'detail': f"blog with id {id} does not exist"}
    return blog

# Delete blog by id
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
   
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return {'response' : 'Blog with id {id} deleted'}


# Update 
@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
   
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found")

    blog.update(request)
    db.commit()
    return 'Updated successfully'


@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(request)
    db.add(new_user)
    db.commit()
    db.refresh()
    return request
