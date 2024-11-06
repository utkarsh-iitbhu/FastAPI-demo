from fastapi import FastAPI, Depends, status, Response, HTTPException
import schemas, models, hashing
from database import engine, SessionLocal
from sqlalchemy.orm import Session 
from typing import List
from passlib.context import CryptContext 

app = FastAPI() 

# Create database table 
models.Base.metadata.create_all(engine)

# Create this func to fetch the db
def get_db():
	db = SessionLocal()
	try: 
		yield db 
	finally:
		db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=['blogs']) # Session Depends on the unc to fetch the db, it wont be a querry param
def create_blog(request: schemas.Blog, db: Session=Depends(get_db)): # we get the db instance 
	new_blog = models.Blog(title=request.title,body=request.body,user_id=1)
	db.add(new_blog)
	db.commit()
	db.refresh(new_blog)
	return new_blog 

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def delete_blog(id, db: Session=Depends(get_db)):
	blog = db.query(models.Blog).filter(models.Blog.id==id)
	if not blog.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found")
	blog.delete(synchronize_session=False)
	db.commit() # Without this it will not comit the delete command
	return {"Detail":f"Blog with {id} is deleted from the database"}

# Without request:schemas.Blog we will not get the Request Body to update our blog
@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update_blog(id, request:schemas.Blog, db:Session=Depends(get_db)):
	blog = db.query(models.Blog).filter(models.Blog.id == id)
	if not blog.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found")
	blog.update(dict(request)) # pass it as a dict object instead of pydantic object
	db.commit()
	return {"Detail":f"Blog with {id} has been updated"}

@app.get('/blog',response_model=List[schemas.ShowBlog],tags=['blogs']) # As we require List of blogs not a single one
def all_blog(db: Session=Depends(get_db)):
	blogs = db.query(models.Blog).all()
	return blogs 

@app.get('/blog/{id}',status_code=201,response_model=schemas.ShowBlog,tags=['blogs'])
def show(id,response:Response, db: Session=Depends(get_db)):
	blog = db.query(models.Blog).filter(models.Blog.id==id).first()
	if not blog:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
					  		detail=f"Blog with the {id} is not found"
						 ) # With this one line of Raise we can implement the below 2 lines 
		# response.status_code = status.HTTP_404_NOT_FOUND
		# return {"Detail":f"Blog with the {id} is not found"}
	return blog

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user',response_model=schemas.ShowUser,tags=['users'])
def create_user(request: schemas.User, db: Session=Depends(get_db)):
	hashedPassword = pwd_context.hash(request.password)
	new_user = models.User(name=request.name,email=request.email,
						   password=hashing.Hash.bcrypt(request.password)
						)
	db.add(new_user)
	db.commit() 
	db.refresh(new_user)
	return new_user

@app.get('/user/{id}',response_model=schemas.ShowUser,tags=['users'])
def get_user(id, db: Session=Depends(get_db)):
	user = db.query(models.User).filter(models.User.id == id).first()
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
	return user 