from fastapi import APIRouter
import database, schemas, models, hashing, oauth
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status, HTTPException
from passlib.context import CryptContext 
from repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/',response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session=Depends(get_db),current_user: schemas.User = Depends(oauth.get_current_user)):
	return user.create(request,db)

@router.get('/{id}',response_model=schemas.ShowUser)
def get_user(id, db: Session=Depends(get_db),current_user: schemas.User = Depends(oauth.get_current_user)):
	return user.show(id,db)