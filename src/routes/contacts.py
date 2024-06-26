from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import ContactCreate, ContactResponse, ContactUpdate
from src.repository import contacts as repository_contacts
from datetime import datetime, timedelta, date

router = APIRouter(prefix='/contacts', tags=["contacts"])


# Select the contacts with birthdate in the next 7 days
@router.get("/birthdays", response_model=List[ContactResponse])
async def get_birthdays(db: Session = Depends(get_db)):
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
    birthdays = await repository_contacts.get_birthdays(today, end_date, db)
    return birthdays


@router.post("/", response_model=ContactCreate)
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(contact, db)


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact_update: ContactUpdate, db: Session = Depends(get_db)):
    updated_contact = await repository_contacts.update_contact(contact_id, contact_update, db)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@router.delete("/{contact_id}")
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    deleted_contact = await repository_contacts.delete_contact(contact_id, db)
    if not deleted_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
        name: str = None, surname: str = None, email: str = None, phone: str = None, birthday: date = None,
        db: Session = Depends(get_db)
):
    contacts = await repository_contacts.get_contacts(name, surname, email, phone, birthday, db)
    return contacts
