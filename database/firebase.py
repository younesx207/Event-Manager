import firebase_admin
from firebase_admin import credentials
from configs.firebase_config_example.py import firebaseConfig
import pyrebase

if not firebase_admin._apps:

    cred = credentials.Certificate("event-calendar-27b62-firebase-adminsdk-6bd1x-c7695f8512.json")

    firebase_admin.initialize_app(cred)

#cred = credentials.Certificate("path/to/serviceAccountKey.json")
#firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()