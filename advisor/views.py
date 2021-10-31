from django.views.decorators.csrf import csrf_exempt
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
import requests
import json
from json import loads
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from .models import Advisor, User, Booking
from django.core.serializers import serialize
from asgiref.sync import async_to_sync, sync_to_async



class DisableCsrfCheck(MiddlewareMixin):

    def process_request(self, req):
        attr = '_dont_enforce_csrf_checks'
        if not getattr(req, attr, False):
            setattr(req, attr, True)


def page_not_found(request):
	return JsonResponse({"mesagge": "404 Page Not Found", "status": False})


async def advisor(request, user_id):

	try:
		res = Advisor()
		res = res.getAdvisor()

		data = list(res)
		for i in res:
			print(i)

		return JsonResponse({"mesagge": data, "status":True},status=200)

	except Exception as e:
		return JsonResponse({"message": str(e), "status":False}, status=404)

#@sync_to_async
@csrf_exempt
#@async_to_sync
def addAdvisor(request):
	try:
		data = request.POST
		advisor = Advisor()
		print(data)

		if request.method == 'POST':
			res = advisor.addAdvisor(data["name"], data["photo"])

			

			"""photo_path = f"media/image/"
			upload_image = data["photo"]
			with open(photo_path,"wb+") as f:
				f.write(upload_image)"""

			# res = advisor.addAdvisor(data["name"])

			return JsonResponse({"message":"Success","status":True},status=200)
		return JsonResponse({"message":"Success","status":True},status=200)
	except Exception as e:
		return JsonResponse({"message": str(e), "status":False}, status=404)


def userRegister(request):
	try:
		data = request.POST
		user = User()
		res = False
		if request.method == 'POST':
			#if user.check_user_already_exist(data["email"]) == True:
			
			# if res == True:
			#	return JsonResponse({"message": "User Already Exist", "status":True}, status=200)
			# else:
			token,user_id = user.register(data["name"], data["email"], data["password"])
			#data = list(res)

			return JsonResponse({"token": token, "user_id": user_id, "status":True}, status=200)

	except Exception as e:
		return JsonResponse({"message": str(e), "status":False}, status=404)


def userLogin(request):
	try:
		data = request.POST
		user = User()

		if request.method == 'POST':
			#token = []
			#user_id = []
			token,user_id = user.login(data["email"], data["password"])
			
			return JsonResponse({"token": token, "user_id": user_id, "status":True}, status=200)

	except Exception as e:
		return JsonResponse({"message": str(e), "status":False}, status=404)


def bookAdvisor(request, user_id, advisor_id):
	try:
		data = request.POST
		booking = Booking()

		if request.method == 'POST':
			res = booking.bookAdvisor(user_id, advisor_id, data["time"])

			return JsonResponse({"status":True}, status=200)

	except Exception as e:
		return JsonResponse({"message": str(e), "status":False}, status=404)


def bookedCalls(request, user_id):
	try:
		booking = Booking()
		
		res = booking.userBookings(user_id)
		data = list(res)

		return JsonResponse({"data": data, "status":True}, status=200)

	except Exception as e:
		return JsonResponse({"message": str(e), "status":False}, status=404)
