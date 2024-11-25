from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.db import SessionLocal
from src.database.models import User
from src.database.db import get_db 
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.repository import contacts
from typing import List
from src.utils import get_current_user
from src.database.models import User
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

router = APIRouter()
templates = Jinja2Templates(directory="static")

# Serve contacts management page
@router.get("/contacts", response_class=HTMLResponse)
def contacts_page(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("contacts.html", {"request": request, "user": current_user.dict()})

# Create a new contact
@router.post("/contacts/", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_contact = contacts.create_contact(db, contact, current_user.id)
    return new_contact

# Get all contacts for the current user
@router.get("/contacts/all", response_model=List[ContactResponse])
def get_all_contacts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return contacts.get_contacts(db, current_user.id)

# Get a specific contact by ID
@router.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_contact = contacts.get_contact(db, contact_id, current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

# Update a contact
@router.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_contact = contacts.update_contact(db, contact_id, contact, current_user.id)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

# Delete a contact
@router.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted_contact = contacts.delete_contact(db, contact_id, current_user.id)
    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return deleted_contact
