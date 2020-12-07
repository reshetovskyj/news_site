from django import forms
from .models import News
import re
from django.core.exceptions import ValidationError
from  django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField
from  django.contrib.auth.models import User


class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст',
                               widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}))

    captcha = CaptchaField()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Імʼя користувача',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Імʼя користувача', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplette': "off"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Підтвердження пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Назва не повинна починатися з цифри')
        return title