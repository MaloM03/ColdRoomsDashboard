from peewee import *
from flask_login import UserMixin
from app.database import db
#from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import os

class BaseModel(Model):
    """Classe de base pour tous les modèles."""
    class Meta:
        database = db

class Role(BaseModel):
    id_roles = AutoField()
    name = CharField(max_length=12, unique=True, null=False)

    class Meta:
        table_name = "roles"

class User(UserMixin, BaseModel):
    id_users = AutoField()
    username = CharField(max_length=25, null=False)
    mail = CharField(max_length=50, unique=True, null=False)
    password_key = CharField(max_length=255, null=False)
    id_roles = ForeignKeyField(Role, backref="users", on_delete="CASCADE")

    def get_id(self):
        return str(self.id_users) 

    class Meta:
        table_name = "users"

    def set_password(self, password):
        """Hacher et stocker le mot de passe avec scrypt."""
        salt = os.urandom(16)  # Génère un sel aléatoire de 16 octets
        hash_value = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1)
        
        self.password_key = f"{salt.hex()}:{hash_value.hex()}"  # Stocke sous forme "salt:hash"
        print(f"Mot de passe enregistré: {self.password_key}")  # Debugging
        self.save()

    def check_password(self, password):
        """Vérifier si le mot de passe correspond au hash stocké."""
        try:
            print(f"Mot de passe stocké: {self.password_key}")  # Debugging
            if ":" not in self.password_key:
                print("Format invalide (pas de ':')")
                return False  # Problème de format

            salt_hex, stored_hash_hex = self.password_key.split(":")  # Séparer sel et hash
            print(f"Salt hex: {salt_hex}")
            print(f"Stored hash hex: {stored_hash_hex}")

            salt = bytes.fromhex(salt_hex)
            stored_hash = bytes.fromhex(stored_hash_hex)

            # Hasher le mot de passe entré avec le même sel
            computed_hash = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1)

            return computed_hash == stored_hash  # Comparaison sécurisée
        except ValueError as e:
            print(f"Erreur de format du mot de passe stocké: {e}")
            return False  # Retourne False en cas d'erreur de format


class Material(BaseModel):
    id_materials = AutoField()
    reference = CharField(max_length=25, null=False)
    name = CharField(max_length=50, null=False)

    class Meta:
        table_name = "materials"

class ColdRoom(BaseModel):
    id_coldroom = AutoField()
    coldroom_name = CharField(max_length=20, null=False)
    max_places = IntegerField(null=True)
    temp_max_limit = DecimalField(max_digits=8, decimal_places=2, null=True)
    temp_min_limit = DecimalField(max_digits=8, decimal_places=2, null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = "coldrooms"

class Temperature(BaseModel):
    id_temperature = AutoField()
    temperature = DecimalField(max_digits=8, decimal_places=2, null=False)
    temp_date = DateTimeField(null=False)
    id_coldroom = ForeignKeyField(ColdRoom, backref="temperatures", on_delete="CASCADE")

    class Meta:
        table_name = "temperatures"

class Alert(BaseModel):
    id_alerts = AutoField()
    name = CharField(max_length=25, null=False)
    comment = CharField(max_length=250, null=False)
    states = IntegerField(null=False, default=0, constraints=[Check("states BETWEEN 0 AND 5")]) 
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")])
    id_coldroom = ForeignKeyField(ColdRoom, backref="alerts", on_delete="CASCADE")

    class Meta:
        table_name = "alerts"

class Location(BaseModel):
    id_materials = ForeignKeyField(Material, backref="locations", on_delete="CASCADE")
    id_coldroom = ForeignKeyField(ColdRoom, backref="locations", on_delete="CASCADE")
    place = IntegerField(null=True)
    quantity = IntegerField(null=True)

    class Meta:
        table_name = "locations"
        primary_key = CompositeKey('id_materials', 'id_coldroom')
