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
    # student_id = models.AutoField(primary_key=True)

    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)


    # def save(self, *args, **kwargs): # Generate Unique ID based on forename and surname
    #     user = User.objects.create_user(self.username, self.email, self.password)
    #     super(Student, self).save(*args, **kwargs)

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
    # defaultID = (str(self.forename)[0]+str(self.surname)[0]).capitalize()

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
    # module_id    = models.AutoField(primary_key=True)

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
    semester  = models.IntegerField(choices=[(1, "Semester 1"), (2, "Semester 2")])


    def clean(self, *args, **kwargs): # Validation to prevent duplicate module instances

        query = []
        try:
            # Check if identical module instance already exists (Shares same module/year/semester)
            query = ModuleInstance.objects.filter(module__exact=self.module).filter(year__exact=self.year).filter(semester__exact=self.semester)
        except Exception as e:
            pass # Exception raised if user hasn't selected a module

        if len(query): # Raise error
            errorMessage = "This module instance already exists. "
            errorMessage+= "Please specify a different year, module or semester to continue."
            raise ValidationError(errorMessage)

        super(ModuleInstance, self).clean(*args, **kwargs)

    def __str__(self):
        toReturn = str(self.module) + ", " + str(self.year) + ", Semester " + str(self.semester)
        toReturn+= ", " + ", ".join([str(p.professorID) for p in self.professor.all()])
        return toReturn
  

class Rating(models.Model):
    ratingChoice = []
    for i in range(1,6,1):
        ratingChoice.append(((i, str(i)+" Stars")))

    instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    student  = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating   = models.FloatField(choices=ratingChoice)

    def __str__(self):
        return str(self.instance.module) + ", " + str(self.student.username) + ", " + str(int(self.rating)) + " stars" 



# from django.db.models.signals import pre_save, post_save

# @ModuleInstance(pre_save)
# def pre_save_handler(sender, instance, *args, **kwargs):
#     # some case
#     if case_error:
#         raise Exception('OMG')
