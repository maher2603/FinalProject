from django.contrib import admin
from .models import User, Vehicle, VehicleLog, Post, Comment, Reply

# Register your models here.
admin.site.register(User)
admin.site.register(Vehicle)
admin.site.register(VehicleLog)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)