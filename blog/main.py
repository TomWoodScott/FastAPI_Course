from fastapi import FastAPI, Depends
from . import schemas
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a blog, add it to the database
@app.post('/blog')
def create(request:schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Return all blogs,  
@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def show_by_id(id, db: Session = Depends(get_db)):
    blog_by_id = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog_by_id