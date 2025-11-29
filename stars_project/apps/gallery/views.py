from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Count, Exists, OuterRef
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.contrib import messages
from .models import Artwork, Category, ArtworkLike
from apps.users.models import UserSearchHistory


@login_required
def dashboard_view(request):
    """User dashboard view"""
    profile = request.user.userprofile
    stats = {
        'artwork_created': profile.artwork_created,
        'level': profile.level,
        'total_xp': profile.total_xp,
    }
    
    context = {
        'profile': profile,
        'stats': stats,
        'recent_artworks': Artwork.objects.filter(artist=request.user).order_by('-created_at')[:5],
    }
    return render(request, 'gallery/dashboard.html', context)

def browse(request):
    """Browse artworks with search and filtering"""
    artworks = Artwork.objects.filter(visibility='public').select_related('artist', 'category').prefetch_related('tags')
    
    if request.user.is_authenticated:
        is_liked = ArtworkLike.objects.filter(
            artwork=OuterRef('pk'),
            user=request.user
        )
        artworks = artworks.annotate(is_liked=Exists(is_liked))
    
    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        artworks = artworks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(artist__username__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
        
        # Save search history for authenticated users
        if request.user.is_authenticated:
            UserSearchHistory.objects.create(
                user=request.user,
                query=search_query,
                search_type='general'
            )
    
    # Category filter
    selected_category = request.GET.get('category', '')
    if selected_category:
        artworks = artworks.filter(category__slug=selected_category)
    
    # Tags filter
    selected_tags = request.GET.get('tags', '').strip()
    if selected_tags:
        tag_list = [tag.strip() for tag in selected_tags.split(',') if tag.strip()]
        for tag_name in tag_list:
            artworks = artworks.filter(tags__name__icontains=tag_name)
    
    # Sort functionality
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'oldest':
        artworks = artworks.order_by('created_at')
    elif sort_by == 'popular':
        artworks = artworks.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')
    elif sort_by == 'views':
        artworks = artworks.order_by('-views', '-created_at')
    elif sort_by == 'likes':
        artworks = artworks.order_by('-likes_count', '-created_at')
    else:  # newest
        artworks = artworks.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(artworks, 24)  # 24 artworks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter
    categories = Category.objects.all().order_by('name')
    
    context = {
        'artworks': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category,
        'selected_tags': selected_tags,
        'sort_by': sort_by,
        'total_count': paginator.count,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'profile': request.user.userprofile if request.user.is_authenticated else None,
    }
    return render(request, 'gallery/browse.html', context)

@login_required
def upload(request):
    """Upload new artwork"""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        category_id = request.POST.get('category')
        tags_str = request.POST.get('tags', '').strip()
        visibility = request.POST.get('visibility', 'public')
        image = request.FILES.get('image')
        
        if not title or not image:
            messages.error(request, 'Title and image are required.')
            return render(request, 'gallery/upload.html', {
                'categories': Category.objects.all().order_by('name'),
                'profile': request.user.userprofile,
            })
        
        # Create artwork
        artwork = Artwork.objects.create(
            title=title,
            description=description,
            image=image,
            artist=request.user,
            visibility=visibility
        )
        
        # Set category
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                artwork.category = category
                artwork.save()
            except Category.DoesNotExist:
                pass
        
        # Process tags
        if tags_str:
            tag_names = [tag.strip().lower() for tag in tags_str.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name,
                    defaults={'slug': tag_name.replace(' ', '-')}
                )
                artwork.tags.add(tag)
        
        # Award XP for upload
        request.user.userprofile.add_xp(50, "Artwork upload")
        
        messages.success(request, f'"{title}" has been uploaded successfully!')
        return redirect('gallery:artwork_detail', pk=artwork.pk)
    
    context = {
        'categories': Category.objects.all().order_by('name'),
        'profile': request.user.userprofile,
    }
    return render(request, 'gallery/upload.html', context)

def artwork_detail(request, pk):
    """View individual artwork"""
    artwork = get_object_or_404(
        Artwork.objects.select_related('artist', 'category').prefetch_related('tags'),
        pk=pk
    )
    
    # Check if artwork is visible to current user
    if artwork.visibility == 'private' and artwork.artist != request.user:
        messages.error(request, 'This artwork is private.')
        return redirect('gallery:browse')
    
    # Record view (only once per session)
    session_key = f'viewed_artwork_{artwork.id}'
    if not request.session.get(session_key):
        artwork.views += 1
        artwork.save(update_fields=['views'])
        request.session[session_key] = True
    
    # Check if user has liked this artwork
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = ArtworkLike.objects.filter(artwork=artwork, user=request.user).exists()
    
    # Get related artworks by the same artist
    related_artworks = Artwork.objects.filter(
        artist=artwork.artist,
        visibility='public'
    ).exclude(pk=artwork.pk).order_by('-created_at')[:4]
    
    context = {
        'artwork': artwork,
        'user_has_liked': user_has_liked,
        'related_artworks': related_artworks,
    }
    return render(request, 'gallery/artwork_detail.html', context)

@login_required
@require_POST
def like_artwork(request, pk):
    """Toggle like on artwork"""
    artwork = get_object_or_404(Artwork, pk=pk)
    
    like, created = ArtworkLike.objects.get_or_create(
        artwork=artwork,
        user=request.user
    )
    
    if not created:
        # Unlike
        like.delete()
        artwork.likes_count = max(0, artwork.likes_count - 1)
        liked = False
    else:
        # Like
        artwork.likes_count += 1
        liked = True
        
        # Award XP to artwork owner
        if artwork.artist != request.user:
            artwork.artist.userprofile.add_xp(5, f"Like received on {artwork.title}")
    
    artwork.save(update_fields=['likes_count'])
    
    return JsonResponse({
        'liked': liked,
        'likes_count': artwork.likes_count
    })
