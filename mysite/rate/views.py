from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Professor, Module, ModuleInstance, Rating
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from functools import wraps

import re



    # # Check if user is logged in via session variables

    # request.session['loggedIn'] #  = True
    # # return request.session.get('loggedIn', False)
    # return 0
# def loginRequired(fn):
#     @wraps(fn)
#     def wrapped(request, *args, **kwargs):
#         print("wowee",request.session['loggedIn'])
#         # return "<b>" + fn(*args, **kwargs) + "</b>"

#     return wrapped

def loginRequired(function):
    def wrap(request, *args, **kwargs):
        
        if request.session.get("loggedIn", False):
            return function(request, *args, **kwargs)

        return redirect("redirect/")


    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

@csrf_exempt
def apiRegister(request): # POST
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
def apiLogin(request):
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
    username = request.POST["username"]
    password = request.POST["password"]

    if len(Student.objects.filter(username__exact=username).filter(password__exact=password)):
        request.session['loggedIn'] = True
        request.session['username'] = username
        return HttpResponse("Welcome!")
    else:
        return HttpResponse("The username or password could not be found.")

@csrf_exempt
@loginRequired
def apiLogout(request):
    '''
    logout
    This causes the user to logout from the current session. The syntax for this command is:
     logout
    '''

    # Get a list of session variables
    keyList = []
    for key in request.session.keys():
        keyList.append(key)

    # Delete session variables
    for key in keyList:
        del request.session[key]

    return HttpResponse("Logout successful.")

@csrf_exempt
@loginRequired
def apiList(request):
    '''
    list
    This is used to view a list of all module instances and the professor(s) teaching each of them (Option
    1 above). The syntax for this command is:
     list
    '''
    
    
    return HttpResponse("\n".join([str(p) for p in ModuleInstance.objects.all()]))

@csrf_exempt
@loginRequired
def apiView(request):
    '''
    view
    This command is used to view the rating of all professors (Option 2 above). The syntax for this
    command is:
     view
    '''
    return HttpResponse('not yet implemented')

@csrf_exempt
@loginRequired
def apiAverage(request):
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





# @loginRequired
@csrf_exempt
@loginRequired
def apiRate(request):
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
    # print(request.session['loggedIn']) #  = True

    return HttpResponse('not yet implemented')

@csrf_exempt
def apiRedirect(request):
    return HttpResponse("You must be logged in to perform that action.")