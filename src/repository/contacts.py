from fastapi import Depends
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate
from datetime import date
from sqlalchemy import extract


# Create a new contact in the database
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Find a contact per ID in the database
async def get_contact(contact_id: int, db: Session):
    return db.query(Contact).filter(Contact.id == contact_id).first()


# Update a contact per ID in the database
async def update_contact(contact_id: int, contact_update: ContactUpdate, db: Session):
    db_contact = await get_contact(contact_id, db)
    if not db_contact:
        return None
    for field, value in contact_update.dict(exclude_unset=True).items():
        setattr(db_contact, field, value)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Delete a contact per ID in the database
async def delete_contact(contact_id: int, db: Session):
    db_contact = await get_contact(contact_id, db)
    if not db_contact:
        return None
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted successfully"}


async def get_birthdays(start_date, end_date, db):
    return db.query(Contact).filter(Contact.birthday.between(start_date, end_date)).all()


async def get_birthdays(start_date: date, end_date: date, db: Session):
    month = extract('month', Contact.birthday)
    day = extract('day', Contact.birthday)
    contacts = db.query(Contact).filter(
        (month == start_date.month) &
        (day >= start_date.day) &
        (day <= end_date.day)
    ).all()
    return contacts


# Search for contacts by name, surname, email or phone
async def get_contacts(
        name, surname, email, phone, birthday, db
):
    query = db.query(Contact)
    if name:
        query = query.filter(Contact.name == name)
    if surname:
        query = query.filter(Contact.surname == surname)
    if email:
        query = query.filter(Contact.email == email)
    if phone:
        query = query.filter(Contact.phone == phone)
    if birthday:
        query = query.filter(Contact.birthday == birthday)
    return query.all()
