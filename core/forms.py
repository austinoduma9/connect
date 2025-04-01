

######################

from django import forms
from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser, Idea, Event
from .models import CustomUser
from django.shortcuts import redirect
from .models import Post, Comment
from .models import Project

##inventor page form
class ProjectForm(forms.ModelForm):
    INDUSTRY_CHOICES = [
    ("tech", "Technology"),
    ("health", "Healthcare"),
    ("finance", "Finance"),
    ("education", "Education"),
    ("energy", "Energy"),
    ]
    industry = forms.ChoiceField(choices=INDUSTRY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Project
        fields = ["title", "description", "industry", "project_image", "website_link"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter idea name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Describe your idea"}),
            "project_image": forms.FileInput(attrs={"class": "form-control"}),
            "website_link": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://example.com"}),
        }

# User Registration Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
            'user_type': forms.Select(attrs={'class': 'form-control'})
        }

# Event Form


#Posts form



##profile edit
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # Your user model
        fields = ["first_name", "last_name", "email", "profile_picture"]  # Customize fields


# from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 4})
    )

##login form
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        label="Password"
    )

##post form
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'industry', 'content', 'image', 'attachment']

        def save(self, commit=True, user=None):
            instance = super().save(commit=False)
            if user:
                instance.user = user
            if commit:
                instance.save()
            return instance
