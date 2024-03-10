from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    prefix="/posts", 
    tags=['Posts']
)


@router.get("/", response_model = List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit: int = 10 , skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    print(limit)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    # print(results)
    # return results
    return posts
    

# @router.get("/posts")
# def get_pasts():
#     cursor.execute("""Select * from posts """)
#     posts = cursor.fetchall()
#     return{"data": posts}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post:schemas.Create_Post, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user) ): 
    # new_post = models.Post(title=post.title, content = post.content, published = post.published)
    
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# @router.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post:Post):
#     cursor.execute(""" insert into posts (title, content, published) values(%s, %s, %s) Returning * """, (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return{'data': new_post}

@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id  {id} not found")
        
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorize to do this operation")
    
    return post

# @router.get("/posts/{id}")
# def get_post(id:int, response: Response):
#     cursor.execute("Select * from posts where id = %s", (str(id)))
#     post = cursor.fetchone()
    
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id  {id} not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return{"message": f"post for id {id} not found"}
        
#     # print(post)
#     return{"post_details": post}


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)

    # deleted_posts = db.query(models.Post).filter(models.Post.id == id).first().delete()

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data for id {id} not found")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorize to do this operation")
    

    post.delete(synchronize_session=False)
    db.commit()

    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# @router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("Delete from  posts where id = %s returning * ", (str(id),))
#     deleted_posts = cursor.fetchone()
#     conn.commit()
    
#     if deleted_posts==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data for id {id} not found")
    
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}")
def update_post(id: int , post:schemas.Create_Post, db: Session = Depends(get_db), response_model = schemas.Posts, current_user : int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data for id {id} not found")
    
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorize to do this operation")
    
    post_query.update(post.dict(), synchronize_session = False)
    db.commit()

    
    return post_query.first()


# @router.put("/posts/{id}")
# def update_post(id:int, post:Post):
#     cursor.execute("Update posts set title = %s, content = %s, published = %s  where id = %s returning *", (post.title, post.content, post.published, str(id)),)
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data for id {id} not found")
    
    
#     return {'message': updated_post}
