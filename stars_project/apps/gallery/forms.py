from django import forms
from .models import Post

# Artwork Upload Form
class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'file_url', 'file_type', 'visibility', 'category']