from django.db.models import Q
from django.forms import modelform_factory
from django.shortcuts import render, redirect

from posts.forms import PostBaseForm, PostDeleteForm, PostCreateForm, SearchBarForm, CommentForm, CommentFormSet
from posts.models import Post


def home_page(request):
    return render(request, 'common/home-page.html')


def dashboard(request):
    search_form = SearchBarForm(request.GET)
    posts = Post.objects.all()

    if request.method == "GET" and search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        posts = posts.filter(
            Q(title__icontains=query)
            |
            Q(content__icontains=query)
            |
            Q(author__icontains=query)
        )



    context = {
        'posts': posts,
        'search_form':search_form
    }

    return render(request, 'posts/dashboard.html', context)


def add_post(request):
    form = PostCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('dashboard')

    context = {
        'form': form
    }
    return render(request, 'posts/add-post.html', context)


def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    form = PostDeleteForm(instance=post)

    if request.method == 'POST':
        post.delete()
        return redirect('dashboard')

    context = {
        'form': form
    }

    return render(request, 'posts/delete-post.html', context)


def details_post(request, pk):
    post = Post.objects.get(pk=pk)

    comment_form = CommentFormSet(request.POST or None)

    if request.method == 'POST' and comment_form.is_valid():
        for form in comment_form:
            comment = form.save(commit=False)
            comment.author = request.user.username
            comment.post = post
            comment.save()
            return redirect('dashboard')

    context = {
        'post': post,
        'comment_form':comment_form
    }

    return render(request, 'posts/post-details.html', context)


def edit_post(request, pk):
    post = Post.objects.get(pk=pk)

    if request.user.is_superuser:
        PostEditForm = modelform_factory(Post,fields="__all__")
    else:
        PostEditForm = modelform_factory(Post,fields=('content',))

    form = PostEditForm(request.POST or None, instance=post)

    if request.method == 'POST' and form.is_valid:
        form.save()
        return redirect('dashboard')

    context = {
        'form': form
    }

    return render(request, 'posts/edit-post.html', context)

