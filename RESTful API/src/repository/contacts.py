from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from src.database.models import Contact, User
from src.schemas import ContactCreate, ContactUpdate

async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Optional[Contact]:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()

async def create_contact(contact: ContactCreate, user: User, db: Session) -> Contact:
    db_contact = Contact(**contact.model_dump(), user_id=user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

async def update_contact(contact_id: int, contact: ContactUpdate, user: User, db: Session) -> Optional[Contact]:
    db_contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if db_contact:
        for key, value in contact.model_dump().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    return None

async def delete_contact(contact_id: int, user: User, db: Session) -> Optional[Contact]:
    db_contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return db_contact
    return None

async def search_contacts(first_name: Optional[str], last_name: Optional[str], email: Optional[str], user: User, db: Session) -> List[Contact]:
    query = db.query(Contact).filter(Contact.user_id == user.id)
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()

async def get_contacts_with_upcoming_birthdays(today: datetime, next_week: datetime, user: User, db: Session) -> List[Contact]:
    today_str = today.strftime('%m-%d')
    next_week_str = next_week.strftime('%m-%d')

    if next_week.year > today.year:
        end_of_year_str = datetime(today.year, 12, 31).strftime('%m-%d')  
        start_of_next_year_str = datetime(next_week.year, 1, 1).strftime('%m-%d')  
        
        contacts = db.query(Contact).filter(
            Contact.user_id == user.id,
            Contact.birthday.isnot(None),
            or_(
                db.func.to_char(Contact.birthday, 'MM-DD').between(today_str, end_of_year_str),
                db.func.to_char(Contact.birthday, 'MM-DD').between(start_of_next_year_str, next_week_str)
            )
        ).all()
    else:
        contacts = db.query(Contact).filter(
            Contact.user_id == user.id,
            Contact.birthday.isnot(None),
            db.func.to_char(Contact.birthday, 'MM-DD').between(today_str, next_week_str)
        ).all()

    return contacts