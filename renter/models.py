from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

ROLE_CHOICES = (
	('Propertyowner', 'Propertyowner'),
	('Renter', 'Renter'),
	)
GENDER_CHOICES =(
	('male', 'male'),
	('female', 'female'),
	)

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone= models.CharField(max_length=12)
    gender=models.CharField(max_length=30, choices=GENDER_CHOICES , null=True)
    birth_date=models.DateField(null=True,blank=True)
    profile_pic=models.ImageField(null=True, blank=True)
    role =models.CharField(max_length=50,choices=ROLE_CHOICES, null=True)



    def __str__(self):
    	# return (self.user.username)
        return str(self.user)+':'+str(self.role)

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()


class Property(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    property_pic=models.ImageField(null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    address=models.CharField(max_length=200)
    price=models.CharField(max_length=200)
    sqft=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
    	return  (self.title)











