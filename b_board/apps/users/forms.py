from django import forms
# from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from allauth.account.forms import LoginForm, SignupForm
from .models import Profile

User = get_user_model()

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not self.instance.pk and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('birth_date', 'avatar')

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
            
            
class MailRegisterForm(SignupForm):
    first_name = forms.CharField(label="Имя",
                                widget=forms.TextInput(attrs={
                                    'type': 'text',
                                    'placeholder': 'Имя',
                                    'class': 'form-control',
                                }), required=False)

    last_name = forms.CharField(label="Фамилия",
                                widget=forms.TextInput(attrs={
                                    'type': 'text',
                                    'placeholder': 'Фамилия',
                                    'class': 'form-control',
                                }), required=False)

    def __init__(self, *args, **kwargs):
        super(MailRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(label="Имя пользователя",
                                widget=forms.TextInput(attrs={
                                'placeholder': 'Имя пользователя',
                                'class': 'form-control',
                                }),)
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторить пароль'})
        self.fields['email'].label = '*Email'
        self.fields['password1'].label = '*Пароль'
        self.fields['password2'].label = '*Повторить пароль'

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if username and User.objects.filter(username=username).exists():
            self.add_error('username', "Пользователь с таким именем уже существует")
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', "Пользователь с таким email уже существует")
            
            
class MailLoginForm(LoginForm):
    
    class Meta:
        model = User
        fields = ('login', 'password')
    def __init__(self, *args, **kwargs):
        self.fields['login'] = forms.CharField(label="Имя пользователя",
                                widget=forms.TextInput(attrs={
                                'placeholder': 'Имя пользователя',
                                'class': 'form-control',
                                }),)
        self.fields['password'].widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Пароль'})
        self.fields['login'].label = '*Логин'
        self.fields['password1'].label = '*Пароль'
    
