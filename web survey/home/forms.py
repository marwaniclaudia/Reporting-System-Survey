from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Createuser(UserCreationForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control form-control-user', 'placeholder':'Password'})
    )
    password2 = forms.CharField(
        label="confirm",
        widget=forms.PasswordInput(attrs={'class':'form-control form-control-user', 'placeholder':'Confirm Password'})
    )
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder':'username'}),
            'first_name':forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder':'firstname'}),
            'last_name':forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder':'lastname'}),
            'email':forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder':'email'}),
        }