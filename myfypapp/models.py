from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class student_record(models.Model):
#     name=models.CharField(max_length=255)
#     company_name=models.CharField(max_length=255)
#     contact=models.CharField(max_length=255)
#     email=models.CharField(max_length=255)
#     address=models.CharField(max_length=255)
    
class Contact(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    company_name=models.CharField(max_length=255)
    tagline=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    contact=models.CharField(max_length=255)

    
    



    
class Pages(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    html = models.TextField()
    css = models.TextField()
    