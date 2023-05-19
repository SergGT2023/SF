from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .tasks import send_new_news


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

class PostCreate(PermissionRequiredMixin,CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('create.Post_Create',)

    def form_valid(self, form):
        Post = form.save(commit=True)
        Post.categoryType ='AR'
        send_new_news.delay()
        return super().form_valid(form)

class PostEdit(PermissionRequiredMixin,UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('create.Post_Edit',)

class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
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

class CategoryList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'category.html'
    context_object_name = 'Сategory'
    paginate_by = 10


@login_required
def add_subscribe(request, pk):
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/')

@login_required
def del_subscribe(request, pk):
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/')