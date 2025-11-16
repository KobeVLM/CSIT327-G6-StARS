from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, UserPreferences


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autofocus": True}))


# To be fixed
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'location', 'website', 'avatar', 'cover_image',
            'instagram_url', 'twitter_url', 'behance_url', 'dribbble_url',
            'is_profile_public', 'show_email_publicly', 'allow_messages',
            'dark_mode', 'language', 'theme_preference',
        ]

# To be Fixed
class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = [
            'artworks_per_page', 'default_sort_order', 'hide_nsfw_content',
            'hide_ai_generated', 'preferred_categories', 'blocked_tags',
            'language', 'timezone'
        ]
