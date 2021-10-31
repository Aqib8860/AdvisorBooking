from datetime import datetime
from Nurturelabs.settings import JWT_SECRET_KEY
import jwt
import random


def generate_tokens(user_id):
    token = jwt.encode({"user_id": user_id}, 'SECRET', algorithm='HS256')
    
    return token


def generate_id(self):
    n = random.randint(1000,9999)
    user_id = "ID"+str(n)+"_"+str(datetime.utcnow().timestamp())
    return user_id

def generate_booking_id(self):
    n = random.randint(1000,9999)
    book_id = "BK"+str(n)+"_"+str(datetime.utcnow().timestamp())
    return book_id
