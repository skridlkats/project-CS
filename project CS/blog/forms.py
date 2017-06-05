from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ( 'Hello_name', 'Task', 'Phone_number', 'Weather', 'Road', 'Data', 'Time_send')

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.is_active = False
            user.save()
        return user


