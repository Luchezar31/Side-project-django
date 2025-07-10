from datetime import datetime

from django.db.models import Q
from django.forms import modelform_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, FormView

from posts.forms import PostBaseForm, PostDeleteForm, PostCreateForm, SearchBarForm, CommentForm, CommentFormSet
from posts.models import Post


# def home_page(request):
#     return render(request, 'common/home-page.html')

class HomePageView(TemplateView):
    # template_name = 'common/home-page.html' # static way

    def get_context_data(self,**kwargs):
        super().get_context_data(**kwargs)
        kwargs.update({
            'current_time':datetime.now()
        })
        return kwargs

    def get_template_names(self):
        if self.request.user.is_superuser:
            return ['common/template_for_admin.html']
        return ['common/home-page.html']

def dashboard(request):
    search_form = SearchBarForm(request.GET)
    posts = Post.objects.order_by('-created_at').all()

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
        'search_form': search_form
    }

    return render(request, 'posts/dashboard.html', context)


# def add_post(request):
#     form = PostCreateForm(request.POST or None, request.FILES or None)
#
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return redirect('dashboard')
#
#     context = {
#         'form': form
#     }
#     return render(request, 'posts/add-post.html', context)


class CreatePost(CreateView):
    form_class = PostCreateForm
    model = Post
    success_url = reverse_lazy('dashboard')
    template_name = 'posts/add-post.html'



# def delete_post(request, pk):
#     post = Post.objects.get(pk=pk)
#     form = PostDeleteForm(instance=post)
#
#     if request.method == 'POST':
#         post.delete()
#         return redirect('dashboard')
#
#     context = {
#         'form': form
#     }
#
#     return render(request, 'posts/delete-post.html', context)

class DeletePost(DeleteView, FormView):
     model = Post
     success_url = reverse_lazy('dashboard')
     template_name = 'posts/delete-post.html'
     form_class = PostDeleteForm

     def get_initial(self):
         pk = self.kwargs.get(self.pk_url_kwarg)
         post = self.model.objects.get(pk=pk)
         return post.__dict__

def details_post(request, pk):
    post = Post.objects.get(pk=pk)

    comment_form = CommentFormSet(request.POST or None)

    if request.method == 'POST' and comment_form.is_valid():
        for form in comment_form:
            comment = form.save(commit=False)
            comment.author = request.user.username
            comment.post = post
            comment.save()
            return redirect('post-details', pk=pk)

    context = {
        'post': post,
        'comment_form': comment_form
    }

    return render(request, 'posts/post-details.html', context)


# def edit_post(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     if request.user.is_superuser:
#         PostEditForm = modelform_factory(Post, fields="__all__")
#     else:
#         PostEditForm = modelform_factory(Post, fields=('content',))
#
#     form = PostEditForm(request.POST or None, instance=post)
#
#     if request.method == 'POST' and form.is_valid:
#         form.save()
#         return redirect('dashboard')
#
#     context = {
#         'form': form
#     }
#
#     return render(request, 'posts/edit-post.html', context)


class EditPost(UpdateView):
    model = Post
    success_url = reverse_lazy('dashboard')
    template_name = 'posts/edit-post.html'

    def get_form_class(self):
        if self.request.user.is_superuser:
            return modelform_factory(Post, fields='__all__')
        return modelform_factory(Post,fields=('content',))