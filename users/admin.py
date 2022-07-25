from django.contrib import admin
from .models import address, customuser

# Register your models here.
admin.site.register(customuser)
admin.site.register(address)
