# Import du framework
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
from documentation.description import api_description


#Import des routers
import routers.router_event


# Initialisation de l'API
app = FastAPI(
    title="Event Manager",
    description=api_description
)

# Model Pydantic = Datatype
class Event(BaseModel):
    id: str
    title: str
    

#L'ajout des routers : 
app.include_router(routers.router_event.router)






