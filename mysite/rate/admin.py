from django.contrib import admin

from .models import Student, Professor, Module, ModuleInstance, Rating
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(ModuleInstance)
admin.site.register(Rating)

