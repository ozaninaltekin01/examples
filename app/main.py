from fastapi import  FastAPI,Response,status,HTTPException,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .database import engine
from . import models,schemas
from .database import get_db
from .schemas import PostCreate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True :
    try:
        conn = psycopg2.connect(
            dbname="fastapi",
            user="postgres",
            password="ozan1234",
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Bağlantı başarılı!")
        break
    except Exception as e:
        print("Bağlantı hatası:", e)
        time.sleep(2)



@app.get("/")
async def root():
    return {"message":"Welcome to my API!"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}



@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate,db: Session = Depends(get_db)):
    """SQL ile direkt olarak post ile veri oluşturma"""

    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   #"(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()

    """SQLAlchemy ile post ile veri oluşturma"""

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{post_id}")
async def get_post_by_id(post_id: int,db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (post_id,))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        return {"data": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.put("/posts/{post_id}",status_code= status.HTTP_200_OK)
async def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db)):
    #cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                   #(post.title, post.content, post.published, post_id))
    #updated_post = cursor.fetchone()
    #conn.commit()

    updated_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    for key,value in post.model_dump(exclude_unset=True).items():
        setattr(updated_post, key, value)

    db.commit()
    db.refresh(updated_post)
    return {"data": updated_post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,
                   #(post_id,))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    deleted_post = (db.query(models.Post).filter(models.Post.id == post_id)
                    .delete(synchronize_session=False))
    db.commit()

    if deleted_post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")