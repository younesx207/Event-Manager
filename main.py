# Import du framework
from fastapi import FastAPI
from documentation.description import api_description


#Import des routers
import routers.router_event
import routers.router_category
import routers.router_user 
import routers.router_stripe


# Initialisation de l'API
app = FastAPI(
    title="Event Manager",
    description=api_description
)


#L'ajout des routers : 
app.include_router(routers.router_event.router)

app.include_router(routers.router_category.router)

app.include_router(routers.router_user.router)

app.include_router(routers.router_stripe.router)






