from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User

# Login Formu
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kullanıcı Adı'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Şifre'
        })
    )

# SignUp Formu
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("profileimage", 'username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'status', 'authorization')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kullanıcı Adı'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adı'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyadı'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'authorization': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': 'name@example.com'}
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Şifre', 'required': True}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Şifreyi Onayla', 'required': True}
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu kullanıcı adı zaten alınmış. Lütfen başka bir kullanıcı adı seçin.")
        return username
    
# SignUpEditForm
class SignUpEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('profileimage', 'username', 'first_name', 'last_name', 'email', 'status', 'authorization')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kullanıcı Adı'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adı'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyadı'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'authorization': forms.Select(attrs={'class': 'form-select'}),
        }
    # Kullanıcı adı kontrolü
    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = self.instance

        # Eğer username değeri değiştiriliyorsa
        if user.username != username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu kullanıcı adı zaten alınmış. Lütfen başka bir kullanıcı adı seçin.")
        
        return username
    
# UpdateUserForm (Şifre Güncelleme Formu)
class UpdateUserForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Yeni Şifre'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifreyi Onayla'})
    )
    
    class Meta:
        model = User
        fields = ('password1', 'password2')

