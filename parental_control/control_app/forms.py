from django import forms
from .models import RestrictedURL

class RestrictedURLForm(forms.ModelForm):
    class Meta:
        model = RestrictedURL
        fields = ['url', 'min_age', 'max_age', 'is_active']




from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'role']