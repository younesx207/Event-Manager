from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from classes.schema_dto import Event, EventNoID
from database.firebase import db
from routers.router_user import get_current_user
from routers.router_stripe import increment_stripe

#api init (launch with uvicorn main:api --reload)
router = APIRouter(
    prefix='/events',
    tags=['Events']
)


# Verbs + Endpoints
@router.get("/", response_model=list[Event])
async def get_event(user_data: int= Depends(get_current_user)):
    queryResults = db.child('users').child(user_data['uid']).child("events").get(user_data['idToken']).val()
    if not queryResults : return []
    eventarray = [value for value in queryResults.values()]
    return eventarray

# 1. Exercice (10min) Create new Student: POST
#connecter la vraie DB (10 min)
#add oauth (10min)
@router.post("/", status_code=201, response_model=Event)
async def create_event(event: EventNoID, user_data: int= Depends(get_current_user)):
    generatedId=str(uuid4())
    newEvent = Event (id=generatedId, title=event.title)
    increment_stripe(user_data['uid'])
    db.child('users').child(user_data['uid']).child("events").child(generatedId).set(data=newEvent.model_dump(), token=user_data['idToken'])
    return newEvent

# 2. Exercice (10min) Student GET by ID
#connecter la vraie DB (10 min)
#add oauth (10min)
@router.get("/{event_id}", response_model=Event)
async def get_event_by_id(event_id: str, user_data: int= Depends(get_current_user)):
    queryResult = db.child('users').child(user_data['uid']).child('events').child(event_id).get(user_data['idToken']).val()
    if not queryResult : raise HTTPException(status_code=404, detail="Event not found") 
    return queryResult

# 3. Exercice (10min) PATCH Student (name)
#connecter la vraie DB (10 min)
#add oauth (10min)
@router.patch("/{event_id}", response_model=Event)
async def event_update(event_id: str, event: EventNoID, user_data: int= Depends(get_current_user)):
    queryResult = db.child('users').child(user_data['uid']).child('events').child(event_id).get(user_data['idToken']).val()
    if not queryResult : raise HTTPException(status_code=404, detail="Student not found") 
    updatedEvent = Event(id=event_id, **event.model_dump())
    return db.child('users').child(user_data['uid']).child('events').child(event_id).update(data=updatedEvent.model_dump(), token=user_data['idToken'])

# 4. Exercice (10min) DELETE Student
#connecter la vraie DB (10 min)
#add oauth (10min)
@router.delete("/{event_id}", status_code=202, response_model=str)
async def event_delete(event_id: str, user_data: int= Depends(get_current_user)) :
    queryResult = db.child('users').child(user_data['uid']).child('events').child(event_id).get(user_data['idToken']).val()
    if not queryResult : 
        raise HTTPException(status_code=404, detail="Event not found")
    db.child('users').child(user_data['uid']).child('events').child(event_id).remove(token=user_data['idToken'])
    return "Event deleted"


#'Students' auront des 'Attendances' pour des 'Sessions'
# utilisateurs, lien vers une ressource
# API vendu à des centre de formations ... 'Center' -> Sessions + Students -> Attendences