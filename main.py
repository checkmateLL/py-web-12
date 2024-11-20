from fastapi import FastAPI
from src.routes import contacts
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(contacts.router, prefix="/api", tags=["contacts"])

#html page to check API
app.mount("/static", StaticFiles(directory="static"), name="static")