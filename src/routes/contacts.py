from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import SessionLocal
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.repository import contacts
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/contacts/", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return contacts.create_contact(db, contact)

@router.get("/contacts/", response_model=List[ContactResponse])
def get_all_contacts(name: str = None, email: str = None, db: Session = Depends(get_db)):
    return contacts.search_contacts(db, name, email)

@router.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = contacts.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.get("/contacts/upcoming-birthdays/", response_model=List[ContactResponse])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    return contacts.get_contacts_with_upcoming_birthdays(db)

@router.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    return contacts.update_contact(db, contact_id, contact)

@router.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    return contacts.delete_contact(db, contact_id)