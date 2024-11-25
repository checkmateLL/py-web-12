from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import SessionLocal
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.repository import contacts
from typing import List
from src.utils import get_current_user
from src.database.models import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/contacts/", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return contacts.create_contact(db, contact, current_user.id)

@router.get("/contacts/", response_model=List[ContactResponse])
def get_all_contacts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return contacts.get_contacts(db, current_user.id)

@router.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_contact = contacts.get_contact(db, contact_id, current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return contacts.update_contact(db, contact_id, contact, current_user.id)

@router.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return contacts.delete_contact(db, contact_id, current_user.id)