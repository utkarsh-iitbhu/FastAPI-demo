from typing import List
from fastapi import APIRouter,Depends,status,HTTPException, Response
import schemas, database, models
import oauth
from sqlalchemy.orm import Session
from repository import blog

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

get_db = database.get_db

@router.get('/',response_model=List[schemas.ShowBlog]) # As we require List of blogs not a single one
def all_blog(db: Session=Depends(get_db),current_user: schemas.User = Depends(oauth.get_current_user)):
	return blog.get_all(db)

@router.post('/',status_code=status.HTTP_201_CREATED,) # Session Depends on the unc to fetch the db, it wont be a querry param
def create_blog(request: schemas.Blog, db: Session=Depends(get_db),current_user: schemas.User = Depends(oauth.get_current_user)): # we get the db instance 
	return blog.create(request,db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session=Depends(get_db),current_user: schemas.User = Depends(oauth.get_current_user)):
	return blog.destroy(id,db)

# Without request:schemas.Blog we will not get the Request Body to update our blog
@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request:schemas.Blog, db:Session=Depends(get_db),current_user: schemas.User = Depends(oauth.get_current_user)):
	return blog.update(id,request,db)

@router.get('/{id}',status_code=201,response_model=schemas.ShowBlog)
def show(id, db: Session=Depends(get_db),current_user: schemas.User = Depends(oauth.get_current_user)):
	return blog.show(id,db)