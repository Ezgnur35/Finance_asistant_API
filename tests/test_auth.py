import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_kayit_basarili(client):
    response = client.post("/auth/register", json={
        "email": "test@gmail.com",
        "password": "123456"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Kayıt başarılı"

def test_ayni_email_tekrar_kayit(client):
    client.post("/auth/register", json={
        "email": "test@gmail.com",
        "password": "123456"
    })
    response = client.post("/auth/register", json={
        "email": "test@gmail.com",
        "password": "123456"
    })
    assert response.status_code == 400

def test_giris_basarili(client):
    client.post("/auth/register", json={
        "email": "test@gmail.com",
        "password": "123456"
    })
    response = client.post("/auth/login", json={
        "email": "test@gmail.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "token" in response.get_json()

def test_yanlis_sifre(client):
    client.post("/auth/register", json={
        "email": "test@gmail.com",
        "password": "123456"
    })
    response = client.post("/auth/login", json={
        "email": "test@gmail.com",
        "password": "yanlis"
    })
    assert response.status_code == 401