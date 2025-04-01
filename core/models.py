from django.contrib.auth.models import AbstractUser

from django.db import models
from django.conf import settings
from django.utils import timezone
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User



##Profile page

class Profile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    profile_pics = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    profile_views = models.IntegerField(default=0)
    inventions = models.ManyToManyField('Invention', blank=True)
    patents = models.ManyToManyField('Patent', blank=True)
    groups = models.ManyToManyField('Group', blank=True)
    pages = models.ManyToManyField('Page', blank=True)
    events = models.ManyToManyField('Event', blank=True)

    def __str__(self):
        # return self.user.username
        return self.user.get_full_name() or self.user.username
        # return self.user.get_full_name() or '_'.join([part.capitalize() for part in self.user.username.split('_')])

    
class Invention(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Patent(models.Model):
    title = models.CharField(max_length=255)
    invention = models.ForeignKey(Invention, on_delete=models.CASCADE)
    date_filed = models.DateField()

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)

# User model with Investor/Innovator roles
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('innovator', 'Innovator'),
        ('investor', 'Investor'),
        ('Admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.username

##intentor page
# class Project(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     industry = models.CharField(max_length=100, choices=[
#         ("tech", "Technology"),
#         ("health", "Healthcare"),
#         ("finance", "Finance"),
#         ("education", "Education"),
#         ("energy", "Energy"),
#     ])
#     project_image = models.ImageField(upload_to="images/", blank=True, null=True)
#     website_link = models.URLField(blank=True, null=True)
    
#     def __str__(self):
#         return self.title
    
##
from django.conf import settings
from django.db import models

class Project(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        default=1  # Default to the user with ID=1, adjust as needed
    )
    title = models.CharField(
        max_length=255, 
        default="Untitled Project"
    )
    description = models.TextField(
        default="No description provided."
    )
    industry = models.CharField(
        max_length=100, 
        choices=[
            ("tech", "Technology"),
            ("health", "Healthcare"),
            ("finance", "Finance"),
            ("education", "Education"),
            ("energy", "Energy"),
        ],
        default="tech"  # Default to 'Technology'
    )
    project_image = models.ImageField(
        upload_to="images/", 
        blank=True, 
        null=True,
        default='images/default.jpg'  # Assuming a default image exists at this location
    )
    website_link = models.URLField(
        blank=True, 
        null=True, 
        default="http://www.example.com"  # Default to an example website
    )
    
    def __str__(self):
        return self.title



#Timezone
class MyModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)


# Model for networking connections


# Model for listing events
    


##patent model

##user groups    
class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(CustomUser)
##user page
class Page(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

# 

##posts

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

def get_default_user():
    User = get_user_model()
    try:
        return User.objects.first().id  # Returns the first user in the database
    except ObjectDoesNotExist:
        return None  # Avoids migration issues if no users exist yet

class Post(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=get_default_user )
    industry = models.CharField(max_length=255, choices=[("IT", "IT"), ("Medicine", "Medicine"), ("Finance", "Finance")])  # Add more industries as needed
    content = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    attachment = models.FileField(upload_to="attachments/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, default="Untitled Post" ) 

    def __str__(self):
        return f"Post by {self.user.username} - {self.industry}"
    


##comments
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

##Who viewed your profile
    

##companies that viewed your profile

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    industry = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company_logos/', default='default_company.png')

    def __str__(self):
        return self.name


##followers
