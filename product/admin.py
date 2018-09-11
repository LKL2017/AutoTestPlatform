from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.

from .models import Product, Status

admin.site.register(Product)
admin.site.register(Status)
