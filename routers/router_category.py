from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from main import Event

router = APIRouter()

categories = []

class Category:
    def __init__(self, name, description):
        self.name = name
        self.description = description

@router.post('/categories')
async def create_category(name: str, description: str):
    new_category = Category(name, description)
    categories.append(new_category)
    return {"message": "Category created successfully"}

@router.get('/categories')
async def get_categories():
    category_data = [{"name": category.name, "description": category.description} for category in categories]
    return category_data