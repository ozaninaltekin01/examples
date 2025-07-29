from fastapi import  FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine
from . import models
from routers import post, user





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

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message":"Welcome to my API!"}




