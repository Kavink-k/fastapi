from pydantic import BaseModel

class Product(BaseModel):
    name:str
    desc:str
    price:int
    quantity:int

 

class User(BaseModel):
    username:str
    password:str