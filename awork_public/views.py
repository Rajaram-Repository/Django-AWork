from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Post, Like, Comment
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import Count,Q,Prefetch
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_data(request,post_id):
    try:
        post = Post.objects.get(pk=post_id)
        json_data = post.json_data
        return JsonResponse({'json_data': json_data}, safe=False)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'No Data'}, status=404)

def all_post(request):

    if request.user.is_authenticated:
        # Retrieve all posts along with their likes and comments count
        search_term = request.GET.get('search', '')
        user = request.user
        if search_term:
            posts_with_counts = Post.objects.filter(
                Q(description__icontains=search_term) | Q(json_data__icontains=search_term)
            ).prefetch_related(
                Prefetch('comment_set', queryset=Comment.objects.all().order_by('-created_at'), to_attr='all_comments'),
                Prefetch('like_set', queryset=Like.objects.filter(user=user), to_attr='user_likes'),
            )
        else:
            posts_with_counts = Post.objects.prefetch_related(
                Prefetch('comment_set', queryset=Comment.objects.all().order_by('-created_at'), to_attr='all_comments'),
                Prefetch('like_set', queryset=Like.objects.filter(user=user), to_attr='user_likes'),
            )
        page = request.GET.get('page', 1)
        paginator = Paginator(posts_with_counts, 2)  # Show 10 posts per page
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        return render(request, 'post.html', {'data': data})
    return render(request, 'post.html')


def insert_post(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        json_data = request.POST.get('json_data', '{}')  
        description = request.POST.get('description', '')
        try:
            json_data_dict = json.loads(json_data)
        except json.JSONDecodeError:
            json_data_dict = {}
            return JsonResponse({ 'message': 'failed'})
        if len(json_data_dict)==2:
            return JsonResponse({ 'message': 'failed'})
        # Get the current user
        user = request.user
        new_post = Post.objects.create(user=user, title=title, json_data=json_data_dict, description=description)

        response_data = {
            'message': 'Post inserted successfully',
            'post_id': new_post.id,
        }

        return JsonResponse(response_data)
    return JsonResponse({ 'message': 'failed'})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    likes_count = Like.objects.filter(post=post).count()
    comments = Comment.objects.filter(post=post)
    
    context = {
        'post': post,
        'likes_count': likes_count,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)

# posts/views.py
# ... (your existing imports)

@csrf_exempt  # Use csrf_exempt for simplicity; consider using csrf protection in a real application
@require_POST
def like_post(request, post_id,like_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    type_like = "Like" if  like_id==0 else "Dislike"
    if Like.objects.filter(post=post, user=user).exists():
        created = Like.objects.filter(post=post, user=user).update(type=type_like)
        if like_id == 0:
            post.like_count += 1
            post.dislike_count -= 1
        else:
            post.like_count -= 1
            post.dislike_count += 1
        post.save()
    else:
        created = Like.objects.create(post=post, user=user,type=type_like)
    
    if created:
        response_data = {'message': 'Post liked successfully'}
    else:
        response_data = {'message': 'You already liked this post'}
    
    return JsonResponse(response_data)

@csrf_exempt  # Use csrf_exempt for simplicity; consider using csrf protection in a real application
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    if request.method == 'POST':
        text = request.POST.get('text', '')
        Comment.objects.create(post=post,  user=user,text=text)
        
        response_data = {'message': 'Comment added successfully'}
        return JsonResponse(response_data)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
