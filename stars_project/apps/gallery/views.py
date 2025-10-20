from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ArtworkForm

# Create your views here.

@login_required
def upload_artwork(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.user = request.user
            artwork.save()
            messages.success(request, 'Artwork uploaded successfully!')
            return redirect('gallery:gallery')
    else:
        form = ArtworkForm()
        
    return render(request, 'gallery/upload.html', {'form': form})


def gallery_view(request):
    """Display all public artworks"""
    from .models import Post
    artworks = Post.objects.filter(visibility='public').order_by('-upload_date')
    return render(request, 'gallery/gallery.html', {'artworks': artworks})
