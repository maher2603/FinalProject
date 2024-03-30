from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model"""
    dob = models.DateField(default=now, null=True)
    profileImage = models.ImageField(null=True, blank=True)

    # Add related names to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username

    def to_dict(self):
        data = {
            'username': self.username,
            'id': self.id,
            'dob': self.dob,
            'profileImage': self.profileImage.url if self.profileImage else None,
            'email': self.email,
        }

        return data

class Vehicle(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20)
    make = models.CharField(max_length=100)
    colour = models.CharField(max_length=50)
    year_of_manufacture = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    engine_capacity = models.IntegerField()
    tax_status = models.CharField(max_length=50)
    tax_due_date = models.DateField()
    mot_status = models.CharField(max_length=50)
    mot_expiry_date = models.DateField()

    def __str__(self):
        return f"{self.registration_number} - {self.user_id}"
    
    def to_dict(self):
        data = {
            'id': self.id,
            'user_id': self.user_id.id,
            'registration_number': self.registration_number,
            'make': self.make,
            'colour': self.colour,
            'year_of_manufacture': self.year_of_manufacture,
            'fuel_type': self.fuel_type,
            'engine_capacity': self.engine_capacity,
            'tax_status': self.tax_status,
            'tax_due_date': self.tax_due_date.strftime('%Y-%m-%d'),
            'mot_status': self.mot_status,
            'mot_expiry_date': self.mot_expiry_date.strftime('%Y-%m-%d'),
        }
        return data
    
class VehicleLog(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    file_upload = models.FileField(upload_to='additional_data_files/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.vehicle_id}"
    
    def to_dict(self):
        data = {
            'id': self.id,
            'vehicle_id': self.vehicle_id.id,
            'title': self.title,
            'date': self.date,
            'cost': self.cost,
            'description': self.description,
            'file_upload': self.file_upload,
        }
        return data