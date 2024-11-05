from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data':{'age':21}}

@app.get('/about')
def about():
    return {'data':{'name':"Sahu"}}

@app.get('/blog')
# limit=10 is the default value if not provided, Optional if u dont want any default value
def index(limit=10, published: bool=True, sort: Optional[str]= None):
    # Only get 10 published blogs
    if published:
        return {"data":f'{limit} published blogs from the db'}
    else:
        return {"data":f'{limit} blogs from the db'}
# We are writting this /blog/un.. before the dynamic /blog/{id} as this will throw error of int
@app.get('/blog/unpublished')
def unpublished():
    return {"data":{"all blogs unpublished"}}

@app.get('/blog/{id}')
def show(id: int):
    # Fetch id of blog 
    return {"data":id}

@app.get('/blog/{id}/comments')
def comments(id):
    # fetch comments of id = id
    return {"data":{'1','2'}}