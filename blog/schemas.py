from pydantic import BaseModel 
from typing import List, Optional

class Blog(BaseModel):
	title: str
	body: str 
	class Config():
		orm_mode = True

class User(BaseModel):
	name: str
	email: str 
	password: str 

class ShowUser(BaseModel):
	name: str
	email: str 
	blogs: List[Blog] = []
	class Config():
		orm_mode = True


# If we pass Blog then all the key-value will be returned
class ShowBlog(BaseModel): # We can use BaseModel and fetch only the feilds that I want
	title: str # With BaseModel I can select which all key-value pairs I want
	body: str
	creator: ShowUser # We are passing the User info as well
	# we are extending the Blog class as we require thr title and body only
	class Config(): # This is from doc of pydantic we need to add this sub-class
		orm_mode = True # Which allows the db to show as it uses sqlalchemy.orm mode 

class Login(BaseModel):
	username: str 
	password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None