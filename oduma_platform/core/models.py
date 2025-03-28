from django.contrib.auth.models import AbstractUser

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model


# User model with Investor/Innovator roles
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('innovator', 'Innovator'),
        ('investor', 'Investor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username
    



#Timezone
class MyModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

# Model for entrepreneurial ideas
class Idea(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('health', 'Healthcare'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ideas")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Model for investors showing interest in ideas
class InvestorInterest(models.Model):
    investor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'investor'})
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('investor', 'idea')

    def __str__(self):
        return f"{self.investor.username} interested in {self.idea.title}"

# Model for networking connections
#Default entry
CustomUser = get_user_model()
class Connection(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    connected_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)  # Replace 1 with a valid user ID

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="connections_made", default=1)
#     connected_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="connections_received")

    class Meta:
        unique_together = ("user", "connected_user")  # No duplicate connections

    def __str__(self):
        return f"{self.user.username} connected with {self.connected_user.username}"

# Model for listing events
class Event(models.Model):
    name = models.CharField(max_length=255)
    # description = models.TextField()
    date = models.DateTimeField()
    # location = models.CharField(max_length=255)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="events")
    created_at = models.DateTimeField(auto_now_add=True)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE , default=1)
    description = models.TextField(blank=True, null=True)  # Add this if missing
    location = models.CharField(max_length=255, blank=True, null=True)  # Add this if missing


    def __str__(self):
        return self.name
    


#Model for profile
class Profile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile/', default='default.jpg')
    company = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=255, blank=True)
    views_count = models.PositiveIntegerField(default=0)  # Track profile views

    def __str__(self):
        return self.user.username

class Invention(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


# class Connection(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     connected_user = models.ForeignKey(CustomUser, related_name="connections", on_delete=models.CASCADE)
#     status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted')])
    


class Patent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    patent_number = models.CharField(max_length=100)
    
class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(CustomUser)

class Page(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

# 


class InvestorProposal(models.Model):
    investor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    about = models.TextField()
    interests = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    reposts = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    image = models.ImageField(upload_to="proposals/", default="default_proposal.jpg")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal by {self.investor.username}"
    

##posts
class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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
        return f"Comment by {self.user.username} on {self.post.id}"
    

##Who viewed your profile
class ProfileView(models.Model):
    viewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="profile_views_made")
    viewed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="profile_views_received")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = ("viewer", "viewed")  # Prevent duplicate views from the same user

    def __str__(self):
        return f"{self.viewer.username} viewed {self.viewed.username}'s profile"
    


##companies that viewed your profile

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    industry = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company_logos/', default='default_company.png')

    def __str__(self):
        return self.name


##followers
class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
    

class Topic(models.Model):
    name = models.CharField(max_length=255)

class Inventor(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()

class Industry(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
