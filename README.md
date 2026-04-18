# Kişisel Finans Asistanı API

Gelir ve gider takibi yapabileceğiniz, kategori bazlı bütçe limitleri belirleyebileceğiniz ve tasarruf hedefleri oluşturabileceğiniz bir REST API projesi. Flask ve SQLAlchemy kullanılarak geliştirildi, JWT ile kimlik doğrulama yapılıyor.

Bu projeyi yaparken özellikle authentication tarafında ve tekrarlı harcama tespitinde zorlandım ama sonunda çalışır hale getirdim. Mobil Mouse projesinde Flask kullandığım için temeli biliyordum, üstüne veritabanı ilişkileri ve güvenlik katmanı ekledim.

## Teknolojiler

- Python, Flask
- SQLAlchemy, SQLite
- Flask-JWT-Extended
- Pytest

## Kurulum

```bash
git clone https://github.com/kullanici-adin/finans-asistani
cd finans-asistani
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## API Endpoint'leri

| Method | URL | Açıklama |
|--------|-----|----------|
| POST | /auth/register | Kullanıcı kaydı |
| POST | /auth/login | Giriş / Token al |
| POST | /kategoriler | Kategori ekle |
| GET | /kategoriler | Kategorileri listele |
| POST | /transactions | İşlem ekle |
| GET | /transactions | İşlemleri listele |
| DELETE | /transactions/<id> | İşlem sil |
| GET | /rapor/aylik | Aylık rapor |
| POST | /limitler | Limit ekle |
| GET | /limitler | Limitleri listele |
| POST | /hedefler | Hedef ekle |
| GET | /hedefler | Hedefleri listele |

## Testler

```bash
pytest -v
```

7 test yazıldı, hepsi geçiyor.

## Proje Yapısı

```
FinanceProject/
├── app/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── transactions.py
│   │   ├── categories.py
│   │   ├── reports.py
│   │   ├── limits.py
│   │   └── goals.py
│   ├── __init__.py
│   └── models.py
├── tests/
│   ├── test_auth.py
│   └── test_transactions.py
├── config.py
├── main.py
└── requirements.txt
```