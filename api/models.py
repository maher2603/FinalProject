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
    
class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    date_posted = models.DateTimeField(default=now)
    image_upload = models.ImageField(upload_to='forum_images/', null=True, blank=True)
    

    def __str__(self):
        return f"{self.user_id.username} - {self.title} - {self.date_posted}"
    
    def to_dict(self):
        data = {
            'id': self.id,
            'user_id': self.user_id.id if self.user_id else None,
            'username': self.user_id.username if self.user_id else None,
            'title': self.title,
            'description': self.description,
            'date_posted': self.date_posted,
            'image_upload': self.image_upload.url if self.image_upload else None, 
        }
        return data 

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=500)
    date_posted = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user_id.username} - {self.comment} - {self.date_posted}"

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.user_id.username,
            'user_id': self.user_id.to_dict(),
            'post_id': self.post_id.id,
            'comment': self.comment,
            'date_posted': self.date_posted,
        }
    
class Reply(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reply = models.CharField(max_length=500)
    date_posted = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user_id.username} - {self.reply} - {self.date_posted} - Reply"

    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.user_id.username,
            'user_id': str(self.user_id.id),
            'comment_id': str(self.comment_id.id),
            'post_id': str(self.comment_id.post_id.id),
            'reply': self.reply,
            'date_posted': self.date_posted,
        }