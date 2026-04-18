import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    Secret_Key =os.getenv('Secret_Key',"gizli_anahtar")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///finans.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY',"jwt_gizli_anahtar")