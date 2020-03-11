from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Professor, Module, ModuleInstance, Rating
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from functools import wraps

import re





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
    '''

    # Check if professor ID exists
    professorID = request.POST["professorID"] # professor_id is the unique id of a professor, and
    professor   = Professor.objects.filter(professorID__exact=professorID)
    if not len(professor):
        return HttpResponse("No professor was found to have the specified ID.")
    # Format of name for printing
    profNameFormat = "Professor " + professor[0].forename[0] + ". " + professor[0].surname + " ("+professor[0].professorID+")"

    # Check if the module code exists
    print("\n\n\n")
    moduleCode  = request.POST["moduleCode"] # module_code is the code of a module.
    module      = Module.objects.filter(code__exact=moduleCode)
    if not len(module):
        return HttpResponse("The module code specified could not be found.")

    # Check if any instances exist for the given module code
    moduleInstanceQuery = ModuleInstance.objects.filter(module__exact=module[0])
    if not len(moduleInstanceQuery):
        return HttpResponse("No module instances could not be found for the specified module code.")

    # Check if professor is present in any of the instances
    instanceList = []
    for instance in moduleInstanceQuery:              # Loop over instances
        for professorObj in instance.professor.all(): # Loop over professors in instance
            if professor[0] == professorObj:
                instanceList.append(instance)         # Create list of valid instances

    # No instances could be found for a given module
    if not len(instanceList):
        return HttpResponse(professor[0]+" was shown not to teach any instances "+module[0]+".")


    ratingCount = 0
    ratingTotal = 0
    for instance in instanceList:
        ratingQuery = Rating.objects.filter(instance__exact=instance).filter(professor__exact=professor[0])
        ratingCount+= len(ratingQuery)
        for rating in ratingQuery:
            ratingTotal += rating.rating


    if not ratingCount:
        return HttpResponse("No ratings were found for "+profNameFormat+" in module "+module[0].title+" ("+module[0].code+")")


    averageRating = round(ratingTotal/ratingCount)
    ratingStars   = averageRating * "*"
    return HttpResponse("The rating of "+profNameFormat+" in module "+module[0].title+" ("+module[0].code+") is "+ratingStars)







@csrf_exempt
@loginRequired
def apiRate(request):
    '''This is used to rate the teaching of a certain professor in a certain module instance (Option 4 above).'''

    # Check rating is a numerical value between 1-5.
    rating = request.POST["rating"]
    if not rating.isnumeric():
        return HttpResponse("Ratings must be numerical values.")
    rating = int(rating)
    if not (1<=rating<=5):
        return HttpResponse("Ratings must be a value between 1-5 stars.")

    # Check semester is a semester number, e.g. 1 or 2
    semester = request.POST["semester"]
    if not semester.isnumeric():
        return HttpResponse("Semesters must be a semester number, e.g. 1 or 2.")
    semester = int(semester)
    if not (1<=semester<=2):
        return HttpResponse("There are only two semesters in an academic year, i.e. Semester 1 - (Autumn) and Semester 2 - (Spring)")

    year = request.POST["year"] # year is a teaching year, e.g. 2018,
    if not year.isnumeric():
        return HttpResponse("Years must be numerical values, e.g. 2018")
    year = int(year)

    module = request.POST["moduleCode"]  # module is the code of a module, e.g. CD1,
    query = ModuleInstance.objects.filter(module__exact=module).filter(year__exact=year).filter(semester__exact=semester)
    if not len(query):
        return HttpResponse("Module instance not found.")


    # professor_id is the UID (unique id) of a professor, e.g. JE1
    # Verify the UID for a professor is present in the given instance
    professorID = request.POST["professorID"]
    professor = 0
    for item in query[0].professor.all():
        if professorID == item.professorID:
            professor=item
            break 

    if not professor: # If no professor found
        return HttpResponse("This module instance is not taught by the specified professor.")

    instance = query[0]
    username = request.session["username"]
    student = Student.objects.filter(username__exact=username)[0]
    query = Rating.objects.filter(instance__exact=instance).filter(student__exact=student).filter(professor__exact=professor)

    # Update students previous rating if rating already exists
    if len(query):
        # Check if the new rating is different to the old one
        if query[0].rating == rating:
            response = "You have already rated "+query[0].professor.professorID+" "+str(rating)+" Stars for this instance."
            return HttpResponse(response)

        # Update the students rating
        response = "Rating updated from "+str(query[0].rating)+" to "+str(rating)+" Stars."
        query[0].rating = rating
        query[0].save()
        return HttpResponse(response)

    # Create new rating
    p1 = Rating.objects.create(
        instance  = instance,
        student   = student,
        professor = professor,
        rating    = rating)

    p1.save()

    return HttpResponse("Rating set successfully")


@csrf_exempt
def apiRedirect(request):
    return HttpResponse("You must be logged in to perform that action.")