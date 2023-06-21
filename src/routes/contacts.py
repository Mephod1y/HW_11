from datetime import date, timedelta
from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact, User
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactModel
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/", response_model=List[ContactResponse], name="All contacts")
async def get_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    return contacts


@router.get("/by_id/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    return contact


@router.get("/search/{text}", response_model=ContactResponse)
async def get_contact_by_text(text: str, db: Session = Depends(get_db),
                              current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contacts_by_lname(text, current_user, db)
    if contact is None:
        contact = await repository_contacts.get_contacts_by_fname(text, current_user, db)
    if contact is None:
        contact = await repository_contacts.get_contact_by_email(text, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.create_contact(body, current_user, db)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Contact is exists!')
    contact = await repository_contacts.create_contact(body, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/birthday/", response_model=List[ContactResponse])
async def week_birthdays(db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts_by_birthday(current_user, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts
