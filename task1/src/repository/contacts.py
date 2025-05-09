from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return (
        db.query(Contact).filter(Contact.user == user).offset(skip).limit(limit).all()
    )


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    contact = (
        db.query(Contact).filter(Contact.id == contact_id, Contact.user == user).first()
    )
    return contact


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        additional_info=body.additional_info,
        user=user,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(
    body: ContactModel, contact_id: int, user: User, db: Session
) -> Contact | None:
    contact = (
        db.query(Contact).filter(Contact.id == contact_id, Contact.user == user).first()
    )
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info
        db.commit()

    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = (
        db.query(Contact).filter(Contact.id == contact_id, Contact.user == user).first()
    )
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def serch_contacts(
    first_name: str, last_name: str, email: str, user: User, db: Session
) -> List[Contact]:
    contacts = db.query(Contact).filter(Contact.user == user)
    if first_name:
        contacts = contacts.filter(Contact.first_name == first_name)

    if last_name:
        contacts = contacts.filter(Contact.last_name == last_name)

    if email:
        contacts = contacts.filter(Contact.email == email)

    return contacts.all()


async def get_upcoming_birthdys(user: User, db) -> List[Contact]:
    today = datetime.today()
    contacts = db.query(Contact).filter(Contact.user == user).all()
    result = []

    for contact in contacts:
        birthday = contact.birthday.replace(year=today.year)
        if today.date() <= birthday <= (today + timedelta(days=7)).date():
            result.append(contact)

    return result
