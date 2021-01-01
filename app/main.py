#the main.py file handles the incoming and outgoing api calls and routes defined in our api.py
from fastapi import FastAPI

from app.api.api import api

app = FastAPI()

app.include_router(api)







