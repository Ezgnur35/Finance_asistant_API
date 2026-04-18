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

@pytest.fixture
def token(client):
    client.post("/auth/register", json={
        "email": "test@gmail.com",
        "password": "123456"
    })
    response = client.post("/auth/login", json={
        "email": "test@gmail.com",
        "password": "123456"
    })
    return response.get_json()["token"]

@pytest.fixture
def kategori(client, token):
    response = client.post("/kategoriler",
        json={"isim": "Yemek"},
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.get_json()["id"]

def test_islem_ekle(client, token, kategori):
    response = client.post("/transactions",
        json={
            "miktar": 150,
            "tur": "gider",
            "kategori_id": kategori,
            "aciklama": "Test harcaması"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

def test_islemleri_getir(client, token, kategori):
    client.post("/transactions",
        json={
            "miktar": 150,
            "tur": "gider",
            "kategori_id": kategori,
            "aciklama": "Test harcaması"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    response = client.get("/transactions",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_token_olmadan_erisim(client):
    response = client.get("/transactions")
    assert response.status_code == 401