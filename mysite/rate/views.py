from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, Professor, Module, ModuleInstance, Rating
import re

@csrf_exempt
def HandleRegisterRequest (request):
    return HttpResponse ('not yet implemented')

@csrf_exempt
def HandleListRequest (request):
    return HttpResponse ('not yet implemented')



@csrf_exempt
def register(request): # POST
    ''' register
    This is used to allow a user to register to the service using a username, email and a password. When
    the command is invoked, the program prompts the user to enter the username, email, and password
    of the new user. The syntax for this command is:

    register
    '''
    def invalidUsername(username): # Ensure the username entered meets username standards

        if Student.objects.filter(username__exact=username): # check if username is taken
            return "The username you have entered is taken"

        if not len(username) or len(username)>=30: # check username length
            return "Username must be between 1 and 30 characters in length."

        return ""


    def invalidPassword(password): # Ensure the password the user entered meets password standards

        if (len(password)<6 or len(password)>=30): # check password length   
            return "Passwords must be between 6 and 30 characters in length."

        return ""

    def invalidEmail(email):
        # Ensure the email entered is valid

        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not re.search(regex,email):
            return "Invalid email."

        return ""

    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]

    check = []
    check.append(invalidUsername(username))
    check.append(invalidPassword(password))
    check.append(invalidEmail(email))

    if (check.count(check[0]) == len(check)): # If there are no errors
        # Create user
        p1 = Student.objects.create(
            username = username,
            password = password,
            email = email)

        p1.save()

        return HttpResponse("User added successfully")
    
    # Concatenate error responses
    response = []
    for item in check:
        if item!="":
            response.append(item)
    return HttpResponse("\n".join([str(p) for p in response]))


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
def listAll(request):
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
    year          is a teaching year, e.g. 2018,
    semester      is a semester number, e.g. 2, and
    rating        is a numerical value between 1-5.
    '''
    return HttpResponse('not yet implemented')