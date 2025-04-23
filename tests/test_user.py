from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == 404

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {'name': 'Alex', 'email': 'alex@mail.com'}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert response.json()['email'] == new_user['email']

def test_create_user_with_invalid_email():
    '''Создание пользователя с существующей почтой'''
    response = client.post("/api/v1/user", json={'name': 'Ivan', 'email': users[0]['email']})
    assert response.status_code == 400

def test_delete_user():
    '''Удаление пользователя'''
    response = client.delete(f"/api/v1/user/{users[0]['id']}")
    assert response.status_code == 200