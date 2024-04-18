from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.todo import ContactSchema, ContactUpdateSchema
from sqlalchemy.sql.expression import or_
from datetime import datetime, timedelta


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    """
    The get_contacts function returns a list of contacts for the given user.
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the offset of the first row to return
    :param db: AsyncSession: Pass the database connection to the function
    :param user: User: Filter the contacts by user
    :return: A list of contact objects
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    """
    The get_all_contacts function returns a list of all contacts in the database.
        
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of contact objects
    :doc-author: Trelent
    """
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    """
    The get_contact function returns a contact from the database.
    
    :param contact_id: int: Filter the results by id
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the user of the contact
    :return: A single contact object
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(id=contact_id, user=user)

    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def search_contact(contact_query: str, db: AsyncSession, user: User):
    """
    The search_contact function searches the database for contacts that match a given query.
        The function takes in two arguments:
            1) contact_query - A string representing the search query to be used when searching for contacts.
            2) db - An asyncpg session object representing an active connection to a PostgreSQL database.  This is used by SQLAlchemy's ORM layer to execute queries against the database.
            3) user - A User object representing the currently logged-in user, which is needed because we only want to return results from their own address book and not anyone else's.
    
    :param contact_query: str: Search for a contact in the database
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Make sure that the user is only able to search for contacts in their own database
    :return: A list of contact objects
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(user=user).filter(
        or_(Contact.first_name.ilike(f"%{contact_query}%"), Contact.last_name.ilike(f"%{contact_query}%"),
            Contact.email.ilike(f"%{contact_query}")))
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    """
    The create_contact function creates a new contact in the database.
    
    :param body: ContactSchema: Validate the request body and deserialize it into a contact object
    :param db: AsyncSession: Create a database session
    :param user: User: Get the user from the request
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)  
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact



async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession, user: User):
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactSchema): A ContactSchema object containing all fields that can be updated for a given user's contacts.
            db (AsyncSession): An async session with an open connection to the database.
            user (User): The User object representing who is making this request, and whose contacts are being updated by it.
    
    :param contact_id: int: Identify the contact that we want to update
    :param body: ContactSchema: Get the data from the request body
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Make sure that the user is only updating their own contacts
    :return: A contact object, which is the same as the body of the request
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info              
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    """
    The delete_contact function deletes a contact from the database.
    
    :param contact_id: int: Identify the contact to be deleted
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Ensure that the user is authorized to delete the contact
    :return: The contact that was deleted
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact



async def contacts_upcoming_birthdays(db: AsyncSession, user: User):
    """
    The contacts_upcoming_birthdays function returns a list of contacts with birthdays in the next week.
    
    :param db: AsyncSession: Pass in the database session
    :param user: User: Filter the contacts by user
    :return: A list of contact objects
    :doc-author: Trelent
    """
    current_date = datetime.now().date()
    week_later = current_date + timedelta(days=7)
    stmt = select(Contact).filter_by(user=user).filter(Contact.birthday.between(current_date, week_later)).order_by(Contact.birthday)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()













