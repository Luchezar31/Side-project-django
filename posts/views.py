from datetime import datetime

from django.db.models import Q
from django.forms import modelform_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, FormView, DetailView, ListView
from django.views.generic.edit import FormMixin

from posts.forms import PostBaseForm, PostDeleteForm, PostCreateForm, SearchBarForm, CommentForm, CommentFormSet
from posts.models import Post


class HomePageView(TemplateView):
    # template_name = 'common/home-page.html' # static way

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        kwargs.update({
            'current_time': datetime.now()
        })
        return kwargs

    def get_template_names(self):
        return ['common/home-page.html']


class Dashboard(ListView):
    template_name = 'posts/dashboard.html'
    model = Post
    paginate_by = 2
    query_param = 'query'
    form_class = SearchBarForm

    def get_context_data(self, *args, **kwargs):
        kwargs.update(
            {
                'search_form': self.form_class(),
                'query': self.request.GET.get(self.query_param)
            }
        )
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.all()
        search_value = self.request.GET.get(self.query_param)

        if search_value:
            queryset = queryset.filter(
                Q(title__icontains=search_value)
                |
                Q(content__icontains=search_value)
                |
                Q(author__icontains=search_value)

            )
        return queryset


class CreatePost(CreateView):
    form_class = PostCreateForm
    model = Post
    success_url = reverse_lazy('dashboard')
    template_name = 'posts/add-post.html'


class DeletePost(DeleteView, FormView):
    model = Post
    success_url = reverse_lazy('dashboard')
    template_name = 'posts/delete-post.html'
    form_class = PostDeleteForm

    def get_initial(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        post = self.model.objects.get(pk=pk)
        return post.__dict__


class DetailPost(DetailView, FormMixin):
    model = Post
    template_name = 'posts/post-details.html'
    form_class = CommentFormSet

    def get_context_data(self, **kwargs):
        kwargs.update({
            'comment_form': self.get_form_class()()
        })

        return super().get_context_data(**kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('post-details', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form_set = self.get_form_class()(request.POST)

        if comment_form_set.is_valid():
            for form in comment_form_set:
                comment = form.save(commit=False)
                comment.author = request.user.username
                comment.post = self.object
                comment.save()
            return self.form_valid(comment_form_set)
        return None


class EditPost(UpdateView):
    model = Post
    success_url = reverse_lazy('dashboard')
    template_name = 'posts/edit-post.html'

    def get_form_class(self):
        if self.request.user.is_superuser:
            return modelform_factory(Post, fields='__all__')
        return modelform_factory(Post, fields=('content',))
