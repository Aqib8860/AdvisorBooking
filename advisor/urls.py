from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from .views import page_not_found, advisor, addAdvisor, userRegister, userLogin, bookAdvisor, bookedCalls

urlpatterns = [
	path('', page_not_found, name='page_no_found'),
	path('user/<str:user_id>/advisor', advisor, name='view-advisor'),
	path('add/advisor', addAdvisor, name='add-advisor'),

	path('user/register', userRegister, name='user-register'),
	path('user/login', userLogin, name='user-login'),

	path('user/<str:user_id>/advisor/booking', bookedCalls, name='view-bookings'),
	path('user/<str:user_id>/advisor/<str:advisor_id>', bookAdvisor, name='book-advisor'),

]
