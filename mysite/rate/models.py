from django.db import models
from django import forms


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
        return str(self.professorID + ", " + self.forename[0] + ". " + self.surname)

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
    for i in range(20):
        yearList.append((2009+i,2009+i))
    
    professor = models.ManyToManyField(Professor)
    module    = models.ForeignKey(Module, on_delete=models.CASCADE)

    # professor = models.CharField(max_length=30)
    year      = models.IntegerField(choices=yearList)
    semester  = models.IntegerField(choices=[(1, "Semester 1"), (2, "Semester 2")])

  

class Rating(models.Model):
    instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    student  = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating   = models.FloatField()



# class ModuleChoiceField(forms.ModelChoiceField):
#      def label_from_instance(self, obj):
#          return "{}: {}".format(obj.module_code, module_title)

# def formfield_for_foreignkey(self, db_field, request, **kwargs):
#     print(db_field.name)
#     if db_field.name == 'module':
#         print("meme")
#         return ModuleChoiceField(queryset=ModuleInstance.objects.all())
#     return super().formfield_for_foreignkey(db_field, request, **kwargs)

# class User(models.Model):
#     username = models.CharField(max_length=30)
#     forename = models.CharField(max_length=30)
#     surname = models.CharField(max_length=30)
#     password = models.CharField(max_length=30)
#     email = models.EmailField(max_length=50)
#     admin = models.BooleanField()
#     accountType = models.IntegerField()
#     averageRating = models.FloatField()

# class ModuleInstance(models.Model):
#     instanceID = models.CharField(max_length=30)
#     module = models.CharField(max_length=30)
#     professor = models.CharField(max_length=30)
#     academicYear = models.DateField()
#     semester = models.IntegerField()
#     averageRating = models.FloatField()

# class Publisher(models.Model):
#   name = models.CharField(max_length=30)
#   address = models.CharField(max_length=50)
#   city = models.CharField(max_length=60)
#   state_province = models.CharField(max_length=30)
#   country = models.CharField(max_length=50)
#   website = models.URLField()


# class Author(models.Model):
#   first_name = models.CharField(max_length=30)
#   last_name = models.CharField(max_length=40)
#   email = models.EmailField()


# class Book(models.Model):
#   title = models.CharField(max_length=100)
#   authors = models.ManyToManyField(Author)
#   publisher = models.ForeignKey(Publisher)
#   publication_date = models.DateField()