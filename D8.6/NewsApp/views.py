import view as view
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .filters import PostFilter
from .forms import PostForm
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostsList(LoginRequiredMixin, ListView):
    model = Post
    ordering = 'text'
    template_name = 'news.html'
    queryset = Post.objects.order_by('-dateCreation')
    context_object_name = 'Posts'
    paginate_by = 10



class PostDetail(DetailView):
    model = Post
    template_name = 'onenews.html'
    context_object_name = 'Post'

class PostCreateNW(PermissionRequiredMixin,CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('create.Post_CreateNW',)

    def form_valid(self, form):
        Post = form.save(commit=True)
        Post.categoryType ='NW'
        return super().form_valid(form)

class PostCreateAR(PermissionRequiredMixin,CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'
    permission_required = ('create.Post_CreateAR',)

    def form_valid(self, form):
        Post = form.save(commit=True)
        Post.categoryType ='AR'
        return super().form_valid(form)

class PostEditNW(PermissionRequiredMixin,UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('create.Post_EditNW',)

class PostEditAR(PermissionRequiredMixin,UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'
    permission_required = ('create.Post_EditAR',)

class PostDeleteNW(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

class PostDeleteAR(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')

class PostsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    queryset = Post.objects.order_by('-dateCreation')
    context_object_name = 'Posts'
    paginate_by = 10

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context