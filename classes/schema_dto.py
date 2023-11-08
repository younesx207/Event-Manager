from pydantic import BaseModel




# Model Pydantic = Datatype
class Event(BaseModel):
    id: str
    title: str
    description: str
    location: str
    date_time: str
    category: str
    
class EventNoID(BaseModel):
    title: str
    description: str
    location: str
    date_time: str
    category: str

class Category(BaseModel):
    id: str
    name: str
    description: str

class CategoryNoID(BaseModel):
    name: str
    description: str

class User(BaseModel):
    email: str
    password: str