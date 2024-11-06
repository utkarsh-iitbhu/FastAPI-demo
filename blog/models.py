from database import Base
from sqlalchemy import Column,Integer,String, ForeignKey
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    body = Column(String)
    # Define a foreign key i.e user.id is mapped to the id in the User model 
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User",back_populates="blogs") # This shows the relationship bw them 


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("Blog",back_populates="creator") # creator and blogs name gets interchanged