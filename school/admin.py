from django.contrib import admin
from .models import Class, CustomUser

# Register your models here.
admin.site.register(Class)
admin.site.register(CustomUser)