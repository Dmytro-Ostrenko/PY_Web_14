from unittest.mock import Mock, AsyncMock, patch

import pytest

from src.services.auth import auth_service
from datetime import datetime, timedelta
from starlette.testclient import TestClient
from main import app
from src.schemas.todo import ContactResponse
from src.entity.models import Contact, User
from src.database.db import get_db
from sqlalchemy.orm import Session



client = TestClient(app)



def test_get_contacts(client, get_token):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0
        
def test_get_all_contacts(client, get_token):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts/all", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0
             


def test_search_upcoming_birthdays(client, get_token):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts/search/upcoming_birthdays", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0
        

# @pytest.fixture
# def test_get_contact_existing_id(client, get_token, monkeypatch):
#     with patch.object(auth_service, 'cache') as redis_mock:
#         redis_mock.get.return_value = None
#         token = get_token
#         headers = {"Authorization": f"Bearer {token}"}
#         session = Session()
#         birthday = datetime.strptime('01.09.2000', '%d.%m.%Y')
#         contact = Contact(id=1,
#             first_name='test_first_name_1',
#             last_name='test_last_name_1',
#             email='test1@gmail.com',
#             phone_number='123456789',
#             birthday=birthday, 
#             additional_info='test_description_1'
#         )
#         session.add(contact)
#         session.commit()
#         response = client.get("/api/contacts/1")
#         assert response.status_code == 200
#         assert isinstance(response.json(), ContactResponse)

def test_get_contact_existing_id(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        birthday = datetime.strptime('01.09.2000', '%d.%m.%Y')
        contact = Contact(
            id=1,
            first_name='test_first_name_1',
            last_name='test_last_name_1',
            email='test1@gmail.com',
            phone_number='123456789',
            birthday=birthday, 
            additional_info='test_description_1'
        )
        with patch('src.routes.routes.get_contact') as mock_get_contact:
            mock_get_contact.return_value = contact
            response = client.get("/api/contacts/1", headers=headers)


def test_get_contact_non_existing_id(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/contacts/999", headers=headers)
        assert response.status_code == 404
        assert response.json() == {"detail": "This Contact not found"}


def test_create_new_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        birthday = datetime.strptime('01.09.2000', '%d.%m.%Y')
        response = client.post("api/contacts", headers=headers, json={            
            "first_name": "testtest",
            "last_name": "TesTes",
            "email": "testtest@example.com",
            "phone_number": "12345678901",
            "birthday": "2001-10-01",
            "additional_info": "test test test test",
        })
        assert response.status_code == 201, response.text
        data = response.json()
        assert "id" in data
        assert data["first_name"] == "testtest"
        assert data["last_name"] == "TesTes"
        assert data["email"] == "testtest@example.com"
        assert data["phone_number"] == "12345678901"
        assert data["birthday"] == "2001-10-01"
        assert data["additional_info"] == "test test test test"

