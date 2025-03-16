from peewee import MySQLDatabase
from app.config import Config

db = MySQLDatabase(
    Config.DB_NAME,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    host=Config.DB_HOST,
    port=Config.DB_PORT
)

def initialize_db():
    if db.is_closed():
        db.connect()
