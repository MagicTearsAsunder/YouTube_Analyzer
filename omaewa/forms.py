from django import forms
from .models import CustomUser, StatsZipFiles


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'password',
            'email'
        ]

    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'maxlength': 50,
            'class': 'form-control',
            'autofocus': 'autofocus'
        })
    )

    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'maxlength': 100,
            'class': 'form-control'
        })
    )

    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={
            'placeholder': 'Email',
            'maxlength': 50,
            'class': 'form-control'
        })
    )


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = StatsZipFiles
        fields = ['file']

    file = forms.FileField(label='', widget=forms.FileInput(
        attrs={
            'aria-describedby': 'inputGroupFileAddon01',
            'id': 'inputGroupFile01',
            'class': 'custom-file-input'
        })
    )
