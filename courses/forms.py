from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from django.forms import ValidationError


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        user = None
        try:
            user = User.objects.get(email=email)
        except:
            return email

        if(user is not None):
            raise ValidationError('User already exists')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=50, required=True, label='Email Address')

    def clean(self):
        email = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = None
        try:
            user = User.objects.get(email=email)
            result = authenticate(username=user.username, password=password)
            if(result is not None):
                return result
            else:
                raise ValidationError('Email or Passowrd is invalid.')
            print('result', result)
        except:
            raise ValidationError('Email or Passowrd is invalid.')
