import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.routes import auth, contacts

app = FastAPI()

# Include routers for authentication and contacts
app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")

# Serve static HTML files - adjusting path to the static folder correctly
static_path = os.path.join(os.path.dirname(__file__), 'static')

if not os.path.exists(static_path):
    raise RuntimeError(f"Static directory '{static_path}' does not exist. Please ensure the correct path is set.")

app.mount("/static", StaticFiles(directory=static_path), name="static")