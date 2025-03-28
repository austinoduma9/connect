

######################

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Idea, Event
from django.shortcuts import redirect
from .models import Post, Comment


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

# Idea Submission Form
class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter idea title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your idea'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

# Event Form
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the event'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event location'})
        }


#Posts form

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["industry", "content", "image", "attachment"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


##profile edit
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # Your user model
        fields = ["first_name", "last_name", "email", "profile_picture"]  # Customize fields


# class ContactForm(forms.Form):
#     name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
#     message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message'}))

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
