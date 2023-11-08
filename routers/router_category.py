from fastapi import APIRouter, Depends, HTTPException, status
from classes.schema_dto import Category,CategoryNoID
from routers.router_user import get_current_user
from uuid import uuid4
from routers.router_stripe import increment_stripe
from database.firebase import db



router = APIRouter(
    prefix='/categories',
    tags=['Category']
)

categories = []

categories_names= set()

#class Category:
    #def __init__(self, name, description):
        #self.name = name
        #self.description = description


@router.get("/", response_model=list[Category])
async def get_category(user_data: int= Depends(get_current_user)):
    queryResults = db.child('users').child(user_data['uid']).child("categories").get(user_data['idToken']).val()
    if not queryResults : return []
    categoryarray = [value for value in queryResults.values()]
    return categoryarray


@router.post('/', status_code=201, response_model=Category)
async def create_category(category: CategoryNoID, user_data: int= Depends(get_current_user)):
    generatedId=str(uuid4())
    newCategory = Category (id=generatedId, name=category.name, description=category.description)
    increment_stripe(user_data['uid'])
    db.child('users').child(user_data['uid']).child("categories").child(generatedId).set(data=newCategory.model_dump(), token=user_data['idToken'])
    categories_names.add(category.name)
    print(categories_names)
    return newCategory

@router.patch("/{category_id}", response_model=Category)
async def category_update(category_id: str, category: CategoryNoID, user_data: int= Depends(get_current_user)):
    queryResult = db.child('users').child(user_data['uid']).child('categories').child(category_id).get(user_data['idToken']).val()
    if not queryResult : raise HTTPException(status_code=404, detail="Category not found") 
    updatedEvent = Category(id=category_id, **category.model_dump())
    return db.child('users').child(user_data['uid']).child('categories').child(category_id).update(data=updatedEvent.model_dump(), token=user_data['idToken'])


@router.delete("/{category_id}", status_code=202, response_model=str)
async def category_delete(category_id: str, user_data: int= Depends(get_current_user)) :
    queryResult = db.child('users').child(user_data['uid']).child('categories').child(category_id).get(user_data['idToken']).val()
    if not queryResult : 
        raise HTTPException(status_code=404, detail="Category not found")
    db.child('users').child(user_data['uid']).child('categories').child(category_id).remove(token=user_data['idToken'])
    category_name_to_delete = queryResult['name']
    if category_name_to_delete in categories_names:
        categories_names.remove(category_name_to_delete)
    else: print("Category name not found in the set")
    return "Category deleted"

#@router.get('/categories')
#async def get_categories():
    #category_data = [{"name": category.name, "description": category.description} for category in categories]
    #return category_data