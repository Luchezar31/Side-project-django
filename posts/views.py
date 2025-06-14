from django.shortcuts import render, redirect

from posts.forms import PostForm
from posts.models import Post


def home_page(request):
    return render(request, 'common/home-page.html')


def dashboard(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }

    return render(request, 'posts/dashboard.html', context)


def add_post(request):
    form = PostForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('dashboard')

    context = {
        'form': form
    }
    return render(request, 'posts/add-post.html', context)
