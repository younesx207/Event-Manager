from ast import List
import uuid
from main import Event
from fastapi import APIRouter, Depends, HTTPException, status



router = APIRouter(
    prefix='/events',
)


events = [
    Event(id="e1", title="test1"),
    Event(id="e2", title="tets2"),
    Event(id="e3", title="test3")
]

# Verbs + Endpoints
@router.get('/events', response_model=List[Event])
async def get_event():
    return events


#reponse 201 --> POST méthode
@router.post('/events', response_model=Event, status_code=201)
async def create_event(event: Event):
    generated_id = str(uuid.uuid4())
    #Creation of the Event obj
    new_event = {
        "id": generated_id,
        "title": event.title,
    }
    #L'ajout de l'Event dans la list
    events.append(new_event)
    return new_event


#GET method to retrieve an event by its ID
# response_model est un Student car nous souhaitons trouvé l'étudiant correspodant à l'ID
@router.get('/events/{event_id}', response_model=Event)
async def get_event_by_ID(event_id:str): 
    #On parcours chaque evenemnent de la liste
    for event in events:
        # Si l'ID correspond, on retourne l'evenement trouvé
        if event.id == event_id:
            return event
    # Si on arrive ici, c'est que la boucle sur la liste "events" n'a rien trouvé
    # HTTP Exception
    raise HTTPException(status_code= 404, detail="Event not found")



#PATCH method to modify an event title by its ID
@router.patch('/events/{event_id}', status_code=204)
async def modify_event_title(event_id:str, modifiedEvent: EventNoID):
    for event in events:
        if event.id == event_id:
            #Modifier le titre de l'evenement
            event.title=modifiedEvent.title
            return
    raise HTTPException(status_code= 404, detail="Event not found")



#DELETE method to delete an event by its ID
@router.delete('/events/{event_id}', status_code=204)
async def delete_event(event_id:str):
    # for loop to find the event 
    for event in events:
        if event.id == event_id:
            #Supprimer l'evenement
            events.remove(event)
            return
    raise HTTPException(status_code= 404, detail="Event not found")