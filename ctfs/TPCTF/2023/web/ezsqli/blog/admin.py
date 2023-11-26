from django.contrib import admin

# Register your models here.
from .models import AdminUser,Blog

admin.site.register(AdminUser)
admin.site.register(Blog)
