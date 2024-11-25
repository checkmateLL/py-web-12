from fastapi import FastAPI
from src.routes import contacts, auth
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(contacts.router, prefix="/api", tags=["contacts"])

#HTML to check API
app.mount("/static", StaticFiles(directory="static"), name="static")