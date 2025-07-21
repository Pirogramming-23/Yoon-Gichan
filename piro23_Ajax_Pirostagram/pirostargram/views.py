from .forms import PostForm
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Post, Comment, PostImage
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import random
import string

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'pirostargram/base.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'pirostargram/content.html', {'post': post, 'user': request.user})

@require_POST
@csrf_protect
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    content = request.POST.get('content')
    if request.user.is_authenticated:
        author = request.user
        nickname = None
    else:
        author = None
        nickname = 'guest_' + ''.join(random.choices(string.digits, k=4))
    if content:
        comment = Comment.objects.create(post=post, content=content, author=author, nickname=nickname)
        comments = post.comments.all()
        return render(request, 'pirostargram/comment.html', {'comments': comments, 'user': request.user})
    return JsonResponse({'error': '내용이 비어 있습니다.'}, status=400)

@require_POST
@csrf_protect
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author and comment.author != request.user:
        return JsonResponse({'error': '권한이 없습니다.'}, status=403)
    comment.delete()
    return JsonResponse({'message': '댓글이 삭제되었습니다.'})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            images = request.FILES.getlist('images')
            for image in images:
                PostImage.objects.create(post=post, image=image)
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'pirostargram/create_post.html', {'form': form})

@require_POST
@csrf_protect
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    session_key = f'liked_post_{pk}'
    liked = request.session.get(session_key, False)
    if liked:
        post.likes.remove(request.user) if request.user.is_authenticated else None
        request.session[session_key] = False
    else:
        post.likes.add(request.user) if request.user.is_authenticated else None
        request.session[session_key] = True
    return JsonResponse({'liked': not liked, 'like_count': post.likes.count()})