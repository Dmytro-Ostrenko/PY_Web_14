import enum
from sqlalchemy import orm
from sqlalchemy import Column, Integer, String, Date, ForeignKey,  Enum, DateTime, func, Boolean
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, date


class Base(orm.DeclarativeBase):
    pass


    
    
class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"

class User(Base):
    __tablename__ = 'users'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(String(50))
    email: orm.Mapped[str] = orm.mapped_column(String(150), nullable=False, unique=True)
    password: orm.Mapped[str] = orm.mapped_column(String(255), nullable=False)
    avatar: orm.Mapped[str] = orm.mapped_column(String(255), nullable=True)    
    refresh_token: orm.Mapped[str] = orm.mapped_column(String(255), nullable=True)
    created_at: orm.Mapped[date] = orm.mapped_column('created_at', DateTime, default=func.now())
    updated_at: orm.Mapped[date] = orm.mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    role: orm.Mapped[Enum] = orm.mapped_column('role', Enum(Role), default=Role.user, nullable=True)
    confirmed: orm.Mapped[bool] = orm.mapped_column(Boolean, default=False, nullable=True)


class Contact(Base):
    __tablename__ = "contacts"   
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    first_name: orm.Mapped[str] = orm.mapped_column(String(20), nullable=False)
    last_name: orm.Mapped[str] = orm.mapped_column(String(20), nullable=False)
    email: orm.Mapped[str] = orm.mapped_column(String(50), nullable=False)
    phone_number: orm.Mapped[str] = orm.mapped_column(String(13), nullable=False)
    birthday: orm.Mapped[str] = orm.mapped_column(Date, nullable=False)
    additional_info: orm.Mapped[str] = orm.mapped_column(String(200))    
    created_at: orm.Mapped[date] = orm.mapped_column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at: orm.Mapped[date] = orm.mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now(), nullable=True)
    user_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user: orm.Mapped["User"] = orm.relationship("User", backref="contacts", lazy="joined")
