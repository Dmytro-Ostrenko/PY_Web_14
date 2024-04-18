import pytest
import unittest
from unittest.mock import MagicMock, AsyncMock, Mock, call
from datetime import datetime, timedelta
from unittest.mock import ANY


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql.expression import or_
from src.entity.models import Contact, User
from src.schemas.todo import ContactSchema, ContactUpdateSchema
from src.repository.todos import create_contact, get_all_contacts, get_contact, update_contact, delete_contact, get_contacts, search_contact, contacts_upcoming_birthdays

class TestAsyncContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(id=1, username='test_user', password="qwerty", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)
    
    async def test_get_all_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contact(id=1, first_name='test_first_name_1', last_name='test_last_name_1', email='test1@gmail.com', phone_number= '123456789', birthday= '01.09.2000', additional_info='test_description_1', user=self.user),
                 Contact(id=2, first_name='test_first_name_2', last_name='test_last_name_2', email='test1@gmail.com', phone_number= '103456780', birthday= '01.09.2001',additional_info='test_description_2', user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_all_contacts(limit, offset, self.session)
        self.assertEqual(result, contacts)
    
    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contact(id=1, first_name='test_first_name_1', last_name='test_last_name_1', email='test1@gmail.com', phone_number= '123456789', birthday= '01.09.2000', additional_info='test_description_1', user=self.user),
                 Contact(id=2, first_name='test_first_name_2', last_name='test_last_name_2', email='test1@gmail.com', phone_number= '103456780', birthday= '01.09.2001',additional_info='test_description_2', user=self.user)]
        mocked_contacts  = Mock()
        mocked_contacts.scalars.return_value.all.return_value = contacts 
        self.session.execute.return_value = mocked_contacts 
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts )


    async def test_get_contact(self):

        user = User(id=1, username='test_user', password="qwerty", confirmed=True)
        contact_id = 1
        contact = Contact(id=contact_id, first_name='test_first_name', last_name='test_last_name', email='test1@gmail.com', phone_number='123456789', birthday='2000-09-01', user=user)
        mocked_contact = Mock()
        mocked_contact.scalar_one_or_none.return_value = contact
        async_session = AsyncMock()
        async_session.execute.return_value = mocked_contact

        result = await get_contact(contact_id, async_session, user)
        assert result == contact
        
    
    

        

    
    async def test_create_contact(self):
        birthday = datetime.strptime('01.09.2000', '%d.%m.%Y')

        body = ContactSchema(
            first_name='test_first_name_1',
            last_name='test_last_name_1',
            email='test1@gmail.com',
            phone_number='123456789',
            birthday=birthday, 
            additional_info='test_description_1'
        )

        result = await create_contact(body, self.session, self.user)

        self.assertIsInstance(result, Contact)
        
        # Перевіряємо, що дані створеного контакту відповідають переданим даним
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.additional_info, body.additional_info)
        
        
    async def test_update_contact(self):
        birthday = datetime.strptime('01.09.2000', '%d.%m.%Y')

        body = ContactSchema(
            first_name='test_first_name_1',
            last_name='test_last_name_1',
            email='test1@gmail.com',
            phone_number='123456789',
            birthday=birthday, 
            additional_info='test_description_1')
        mocked_contact = MagicMock()
        
        mocked_contact.scalar_one_or_none.return_value = Contact(
        id=1, 
        first_name='test_first_name_1', 
        last_name='test_last_name_1', 
        email='test1@gmail.com', 
        phone_number='123456789', 
        birthday='01.09.2000', 
        additional_info='test_description_1', 
        user=self.user)              
            
        self.session.execute.return_value = mocked_contact
        result = await update_contact(1, body, self.session, self.user)            
        self.assertIsInstance(result, Contact)            
        # Перевіряємо, що дані створеного контакту відповідають переданим даним
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.additional_info, body.additional_info)
        
    async def test_delete_contact(self):
        mocked_contact = MagicMock()
        
        mocked_contact.scalar_one_or_none.return_value = Contact(
        id=1, 
        first_name='test_first_name_1', 
        last_name='test_last_name_1', 
        email='test1@gmail.com', 
        phone_number='123456789', 
        birthday='01.09.2000', 
        additional_info='test_description_1', 
        user=self.user)    
        
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()

        self.assertIsInstance(result, Contact)
        


    async def test_search_contact(self):
        contact_query = "test"
        user = User(id=1, username='test_user', password="qwerty", confirmed=True)
        contacts = [
            Contact(id=1, first_name='test_first_name_1', last_name='test_last_name_1', email='test1@gmail.com', phone_number='123456789', birthday='01.09.2000', additional_info='test_description_1', user=user),
            Contact(id=2, first_name='other_first_name', last_name='other_last_name', email='other@gmail.com', phone_number='987654321', birthday='02.09.2000', additional_info='other_description', user=user)
        ]

        mocked_contacts = MagicMock()

        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        search_result = await search_contact(contact_query, self.session, user)
        self.session.execute.assert_called_once()
        self.assertEqual(search_result, contacts)
        
        
        

    async def test_contacts_upcoming_birthdays(self):

        user = User(id=1, username='test_user', password="qwerty", confirmed=True)
        current_date = datetime.now().date()
        week_later = current_date + timedelta(days=7)
        contacts = [
            Contact(id=1, first_name='test_first_name_1', last_name='test_last_name_1', email='test1@gmail.com', phone_number='123456789', birthday=current_date, user=user),    
            Contact(id=2, first_name='other_first_name', last_name='other_last_name', email='other@gmail.com', phone_number='987654321', birthday=week_later, user=user)
        ]
        
        mocked_session = AsyncMock()
        
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        mocked_session.execute.return_value = mocked_contacts

        result = await contacts_upcoming_birthdays(mocked_session, user)

        expected_stmt = select(Contact).filter_by(user=user).filter(Contact.birthday.between(current_date, week_later)).order_by(Contact.birthday)
        mocked_session.execute.assert_called_once_with(ANY)

        mocked_contacts.scalars.assert_called_once_with()
        assert result == contacts

        

