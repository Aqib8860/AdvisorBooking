from django.db import models
from Nurturelabs.settings import clientOpen
from datetime import datetime
import hashlib
from .auth import generate_tokens, generate_id, generate_booking_id
import jwt
import json
#from bson.json_utils import loads, dumps

# Create your models here.

class Advisor:
	def __init__(self):
		self.client = clientOpen()

	def getAdvisor(self):
		res = self.client.advisor.profile.find()
		self.client.close()
		return res

	def addAdvisor(self, name, photo):
		self.client.advisor.profile.insert({
			"_id": name+"_"+str(datetime.utcnow().timestamp()),
			"name": name,
			"photo": photo,
		})
		self.client.close()
		return name


class User:
	def __init__(self):
		self.client = clientOpen()

	async def hash_password(password: str):
	    return base64.b64encode(hashlib.pbkdf2_hmac(
	        'sha256', # The hash digest algorithm for HMAC
	        password.encode('iso-8859-1'), # Convert the password to bytes
	        SECURITY.SECRET_KEY.encode("iso-8859-1"), # Provide the salt
	        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
	    ))

	def check_user_already_exist(self, email):
		if self.client.auth.profile.find({"email": email}):
			return True
		else:
			return False

	def register(self, name, email, password):
		user_id = generate_id(name)

		self.client.auth.profile.insert_one({
			"_id": user_id,
			"name": name,
			"email": email,
			"password": password,
		})
		
		token = generate_tokens(user_id)
		self.client.auth.token.insert_one({"_id": user_id, "token":token})
		
		return token,user_id

	def login(self, email, password):
		user_id = self.client.auth.profile.find({
			"email": email,
			"password": password
		}, {"_id"})
		
		#token = generate_tokens(user_id)
		#self.client.auth.token.insert_one({"_id": user_id, "token":token})
		#user = list(user)
		#token = generate_tokens(user)
	
		#token = list(self.client.auth.token.find({"_id": user_id}, {"token"}))
		
		token = generate_tokens(user_id)
		self.client.auth.token.insert_one({"_id": user_id, "token":token})
		# token = list(token)
		# user = list(user)
		# token = json.loads(token)
		# token = json.dumps(token)

		# user_id = json.loads(user_id)
		# user_id = json.dumps(user_id)
		return token, user_id


class Booking:
	def __init__(self):
		self.client = clientOpen()

	def bookAdvisor(self, user_id, advisor_id, time):
		book_id = generate_booking_id(user_id)
		res = self.client.advisor.booking.insert_one({
			"_id": book_id,
			"user_id": user_id,
			"advisor_id": advisor_id,
			"time": time
		})
		return True

	def userBookings(self, user_id):
		bookings = self.client.advisor.booking.find({
			"user_id": user_id
		})
		return bookings
