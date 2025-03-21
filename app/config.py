from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = "votre_cle_secrete_longue_et_random"
    DB_NAME = os.getenv("DB_NAME", "coldroom_db")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
