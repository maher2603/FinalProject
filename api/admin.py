from django.contrib import admin
from .models import User, Vehicle, VehicleLog

# Register your models here.
admin.site.register(User)
admin.site.register(Vehicle)
admin.site.register(VehicleLog)