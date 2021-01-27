from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class userForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','password1','password2','email']


class volunteerForm(UserCreationForm):
    phone = forms.CharField(max_length=15, min_length=10,required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'password1','password2','email', 'phone' ]