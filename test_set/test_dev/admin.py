from django.contrib import admin
from .models import Task

# Register your models here.
# class RegisterTask(admin.ModelAdmin):
#     list_display = ['numberTask','status']

admin.site.register(Task)
