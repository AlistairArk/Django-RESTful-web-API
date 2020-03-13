from django.db import models
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Student(models.Model):
    '''
    Users of the service (students) can rate professors but cannot add or change module information.
    Before they can rate professors, users must register by providing a username, email, and password.
    Users can only rate professors when they are logged in to the service. 
    '''

    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)

    def clean(self, *args, **kwargs): # Validation to prevent duplicate module instances
        # Error check to prevent duplicate users from being entered via admin
        query = []
        try:
            # Check if identical user instance already exists (Shares same username)
            query = Student.objects.filter(username__exact=self.username)
        except Exception as e:
            pass # Exception raised if user hasn't selected a module

        if len(query): # Raise error
            # Dont allow duplicate users/ Remove previous instance if it already exists
            query[0].delete()
            print("removing dupe")


        super(Student, self).clean(*args, **kwargs)


    def __str__(self):
        return str(self.username + ", " + self.email)



class Professor(models.Model):
    '''
    The overall rating of a professor is the average of the professor’s rating by all users across all
    module instances taught by this professor
    '''
    forename = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    professorID = models.CharField(max_length=30, editable=False)


    def save(self, *args, **kwargs): # Generate Unique ID based on forename and surname
        uid = str(self.forename)[0] + str(self.surname)[0]  # Unique ID

        # Check for users with matching ID start
        uidSet = Professor.objects.filter(professorID__contains=uid)
        uidLen = len(uidSet)
        uid += str(uidLen)

        self.professorID = uid
        super(Professor, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.professorID + ", Professor " + self.forename[0] + ". " + self.surname)


class Module(models.Model):
    code  = models.CharField(max_length=30, primary_key=True)
    title = models.CharField(max_length=30)

    def __str__(self):
        return str(self.code + ": " + self.title)


class ModuleInstance(models.Model):
    '''
    A module instance is a module taught in a certain year and semester by one or more
    professors. Any decimal fraction in the average is rounded to the nearest integer.
    '''
    # instance_id  = models.AutoField(primary_key=True)
    yearList = []
    for i in range(2000,3000,1):
        yearList.append((i,i))
    
    professor = models.ManyToManyField(Professor)
    module    = models.ForeignKey(Module, on_delete=models.CASCADE)
    year      = models.IntegerField(choices=yearList)
    semester  = models.IntegerField(choices=[(1, "Semester 1 - (Autumn)"), (2, "Semester 2 - (Spring)")])


    def clean(self, *args, **kwargs): # Validation to prevent duplicate module instances
        query = []
        try:
            # Check if identical module instance already exists (Shares same module/year/semester)
            query = ModuleInstance.objects.filter(module__exact=self.module).filter(year__exact=self.year).filter(semester__exact=self.semester)
        except Exception as e:
            pass # Exception raised if user hasn't selected a module

        if len(query): # Raise error
            # Dont allow duplicate module instances / Remove previous instance if it already exists
            query[0].delete()
            print("removing dupe")

           
        super(ModuleInstance, self).clean(*args, **kwargs)

    def __str__(self):
        toReturn = str(self.module.title) + " (" + str(self.module.code) + ")" 
        toReturn+= ", Semester " + str(self.semester) + ", Year " + str(self.year) 
        toReturn+= ", Taught by " + ", ".join([str(p.professorID) for p in self.professor.all()])
        return toReturn
  

class Rating(models.Model):
    ratingChoice = []
    for i in range(1,6,1):
        ratingChoice.append(((i, str(i)+" Stars")))

    instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    student  = models.ForeignKey(Student, on_delete=models.CASCADE)
    professor= models.ForeignKey(Professor, on_delete=models.CASCADE)
    rating   = models.IntegerField(choices=ratingChoice)

    def clean(self, *args, **kwargs): # Validation to prevent duplicate module instances

        errorMessage = ""
        try:
            # Verify the UID for a professor is present in the given instance
            profFound = 0
            for item in self.instance.professor.all():
                if self.professor == item:
                    profFound = 1
                    break 

            if not profFound:
                errorMessage = str(self.professor) + " does not teach " + str(self.instance) + ". "
                raise

            else:
                query = Rating.objects.filter(instance__exact=self.instance).filter(student__exact=self.student).filter(professor__exact=self.professor)
                # Dont allow duplicate ratings / Remove previous rating if it already exists
                if len(query):
                    query[0].delete()

        except Exception as e:
            if errorMessage != "":
                raise ValidationError(errorMessage)

        super(Rating, self).clean(*args, **kwargs)


    def __str__(self):
        instanceName = str(self.instance.module) + ", " + str(self.instance.year) + ", Semester " + str(self.instance.semester)

        return str(self.student.username) +  " rated "  + str(self.professor.professorID) + " " + str(int(self.rating)) + " stars for " + instanceName


