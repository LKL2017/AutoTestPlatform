from django.contrib import admin

# Register your models here.

from .models import Users, Privileges

admin.site.register(Users)
admin.site.register(Privileges)
