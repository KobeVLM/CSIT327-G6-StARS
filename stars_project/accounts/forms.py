from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post

class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'johndoe123'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'johndoe@gmail.com'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'John'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Doe'}), required=False)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': '********'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'placeholder': '********'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'file_url', 'file_type', 'visibility', 'category']