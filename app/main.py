# from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends

# from pydantic import BaseModel
# from random import randrange
# import psycopg2
from psycopg2.extras import RealDictCursor
# import time
from sqlalchemy.orm import Session
from . import models, schemas , utils
from .database import engine, SessionLocal
from .routers import post, user, auth, votes
from .database import get_db
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


print(settings.database_username)

# models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],

)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@app.get("/sqlalchemy")
def test_posts( db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# while True:

#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user='postgres', password='Devanshu@1234', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull")
#         break

#     except Exception as error:
#         print("connecting to database failed")
#         print ("error was ", error)
#         time.sleep(3)


# my_posts = [{"title": "title of post", "context": "context of page", "id": 1}, 
#             {"title": "favorite foods", "context": "I love pizza", "id": 2}]



@app.get("/")
def read_root():
    return {"Hello": "World"}




# def find_posts(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p


# @app.get("/posts", response_model = List[schemas.Posts])
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts
    

# # @app.get("/posts")
# # def get_pasts():
# #     cursor.execute("""Select * from posts """)
# #     posts = cursor.fetchall()
# #     return{"data": posts}


# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model = schemas.Posts)
# def create_posts(post:schemas.Post, db : Session = Depends(get_db) ):
#     # new_post = models.Post(title=post.title, content = post.content, published = post.published)
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post


# # @app.post("/posts", status_code=status.HTTP_201_CREATED)
# # def create_posts(post:Post):
# #     cursor.execute(""" insert into posts (title, content, published) values(%s, %s, %s) Returning * """, (post.title, post.content, post.published))
# #     new_post = cursor.fetchone()
# #     conn.commit()
# #     return{'data': new_post}

# @app.get("/posts/{id}", response_model = schemas.Posts)
# def get_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()



#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id  {id} not found")
        
#     return post

# # @app.get("/posts/{id}")
# # def get_post(id:int, response: Response):
# #     cursor.execute("Select * from posts where id = %s", (str(id)))
# #     post = cursor.fetchone()
    
# #     if not post:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id  {id} not found")
# #         # response.status_code = status.HTTP_404_NOT_FOUND
# #         # return{"message": f"post for id {id} not found"}
        
# #     # print(post)
# #     return{"post_details": post}


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db:Session = Depends(get_db)):

#     post = db.query(models.Post).filter(models.Post.id == id)

#     # deleted_posts = db.query(models.Post).filter(models.Post.id == id).first().delete()

#     if post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data for id {id} not found")
    
#     post.delete(synchronize_session=False)
#     db.commit()

    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)



# # @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# # def delete_post(id: int):
# #     cursor.execute("Delete from  posts where id = %s returning * ", (str(id),))
# #     deleted_posts = cursor.fetchone()
# #     conn.commit()
    
# #     if deleted_posts==None:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data for id {id} not found")
    
    
# #     return Response(status_code=status.HTTP_204_NO_CONTENT)



# @app.put("/posts/{id}")
# def update_post(id: int , post:schemas.Post, db: Session = Depends(get_db), response_model = schemas.Posts):

#     post_query = db.query(models.Post).filter(models.Post.id == id)

#     if post_query.first()==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data for id {id} not found")
    
#     post_query.update(post.dict(), synchronize_session = False)
#     db.commit()

    
#     return post_query.first()


# # @app.put("/posts/{id}")
# # def update_post(id:int, post:Post):
# #     cursor.execute("Update posts set title = %s, content = %s, published = %s  where id = %s returning *", (post.title, post.content, post.published, str(id)),)
# #     updated_post = cursor.fetchone()
# #     conn.commit()
# #     if updated_post==None:
# #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data for id {id} not found")
    
    
# #     return {'message': updated_post}



# @app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# def create_user(user: schemas.User, db:Session=Depends(get_db) ):
#     user.password = utils.hash(user.password)
#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user


# @app.get("/users/{id}" , response_model=schemas.UserOut)
# def get_user(id:int , db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
    
#     if not user: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    
#     return user
