from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password'
        })
    )

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("profileimage",'username','first_name','last_name','email',
                  'password1','password2','status','authorization','profileimage'
        )
        widgets ={
            'username' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'kullanıcı adı'},),
            'first_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'adı'},),
            'last_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'soyadı'},),
            'status' : forms.Select(attrs={'class': 'form-select'},),
            'authorization' : forms.Select(attrs={'class': 'form-select'},),
        }
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': 'name@example.com'}
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm password','required': 'required'}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm password','required': 'required'}

class SignUpEditForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    
   
    class Meta:
        model = User
        fields = ('profileimage','username','first_name','last_name',
                  'email','status','authorization',
        )

class UpdateUserForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    class Meta:
        model = User
        fields = ('password1','password2')
    
