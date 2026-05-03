from datetime import datetime
from db import users_collection
import bcrypt

def create_user(name,email,password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }
    users_collection.insert_one(user)


def find_user_by_email(email):
    return users_collection.find_one({"email": email})

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)