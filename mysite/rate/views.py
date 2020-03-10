from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse


@csrf_exempt
def HandleRegisterRequest (request):
	return HttpResponse ('not yet implemented')

@csrf_exempt
def HandleListRequest (request):
	return HttpResponse ('not yet implemented')


@csrf_exempt
def register(request):
	''' register
	This is used to allow a user to register to the service using a username, email and a password. When
	the command is invoked, the program prompts the user to enter the username, email, and password
	of the new user. The syntax for this command is:

	register
	'''
	
	# username
	# password
	# email
	# p1 = Professor.objects.create( forename = '',	surname = '',
	# 	password = '',
	# 	email = '',
	# 	admin = '',
	# 	accountType = '',
	# 	averageRating = '')

	# p1.save()

	# p1 = Professor.objects.create(username = '',
	# 	forename = '',
	# 	surname = '',
	# 	password = '',
	# 	email = '',
	# 	admin = '',
	# 	accountType = '',
	# 	averageRating = '')

	# p1.save()

	# User.objects.all()
	# User

	return HttpResponse('not yet implemented')

@csrf_exempt
def login(request):
	''' login
	This command is used to log in to the service. The syntax for this command is:

	login url 

	where:
	url is the address of the service. Since you will be hosting your web service at
	www.pythonanywhere.com, this should be something like ‘xxxxxx.pyhtonanywhere.com’, where
	xxxxxx is your university username.
	Invoking this command will prompt the user to enter a username and password which are then sent
	to the service for authentication.
	'''
	return HttpResponse('not yet implemented')

@csrf_exempt
def logout(request):
	'''
	logout
	This causes the user to logout from the current session. The syntax for this command is:
	 logout
	'''
	return HttpResponse('not yet implemented')

@csrf_exempt
def list(request):
	'''
	list
	This is used to view a list of all module instances and the professor(s) teaching each of them (Option
	1 above). The syntax for this command is:
	 list
	'''
	return HttpResponse('not yet implemented')

@csrf_exempt
def view(request):
	'''
	view
	This command is used to view the rating of all professors (Option 2 above). The syntax for this
	command is:
	 view
	'''
	return HttpResponse('not yet implemented')

@csrf_exempt
def average(request):
	'''
	average
	This command is used to view the average rating of a certain professor in a certain module (Option 3
	above). The syntax of the command is:
	 average professor_id module_code
	where:
	professor_id is the unique id of a professor, and
	module_code is the code of a module.
	'''
	return HttpResponse('not yet implemented')

@csrf_exempt
def rate(request):
	'''
	rate
	This is used to rate the teaching of a certain professor in a certain module instance (Option 4 above).
	It has the following syntax:

	professor_id  is the unique id of a professor, e.g. JE1,
	module_code   is the code of a module, e.g. CD1,
	year 		  is a teaching year, e.g. 2018,
	semester 	  is a semester number, e.g. 2, and
	rating 		  is a numerical value between 1-5.
	'''
	return HttpResponse('not yet implemented')