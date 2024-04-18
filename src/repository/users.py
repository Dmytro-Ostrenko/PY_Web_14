from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import libgravatar 

from src.database.db import get_db
from src.entity.models import User
#from src.schemas.todo import ContactSchema
from src.schemas.user import UserSchema


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    The get_user_by_email function returns a user object from the database based on the email address provided.
        If no user is found, None is returned.
    
    :param email: str: Pass in the email of the user that we want to retrieve
    :param db: AsyncSession: Pass in the database session
    :return: A user object if the email exists in the database
    :doc-author: Trelent
    """
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    The create_user function creates a new user in the database.
    
    :param body: UserSchema: Validate the data sent in the request body
    :param db: AsyncSession: Pass in the database session
    :return: A user object
    :doc-author: Trelent
    """
    avatar = None
    try:
        g = libgravatar.Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    The update_token function updates the user's refresh token in the database.
    
    :param user: User: Get the user object from the database
    :param token: str | None: Pass the token to the function
    :param db: AsyncSession: Pass the database session to the function
    :return: Nothing, but the type hints say it returns a user
    :doc-author: Trelent
    """
    user.refresh_token = token
    await db.commit()
    
async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    The confirmed_email function marks a user as confirmed in the database.
    
    :param email: str: Get the email of the user that is going to be confirmed
    :param db: AsyncSession: Pass the database session to the function
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()
    
async def update_avatar(email: str, url: str | None, db: AsyncSession) -> User:
    """
    The update_avatar function updates the avatar of a user.
    
    Args:
        email (str): The email address of the user to update.
        url (str | None): The URL to set as the new avatar for this user, or None if no change is desired.
        db (AsyncSession): An async database session object used for querying and updating data in our database.  This should be an instance of AsyncSession from sqlalchemy_aio, not a regular SQLAlchemy Session object!  See https://github.com/klen/sqlalchemy-aio#usage
    
    :param email: str: Find the user in the database
    :param url: str | None: Specify that the url parameter can be either a string or none
    :param db: AsyncSession: Pass the database session to the function
    :return: A user object, which is the same as what get_user_by_email returns
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user
