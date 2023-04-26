from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    model = Post
    ordering = 'text'
    template_name = 'news.html'
    queryset = Post.objects.order_by('-dateCreation')
    context_object_name = 'Posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'onenews.html'
    context_object_name = 'Post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context
    from django.core.paginator import Paginator
from django.shortcuts import render
from .models import News

def news(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 10) # показывать по 10 новостей на странице
    page = request.GET.get('page')
    news = paginator.get_page(page)
    return render(request, 'news.html', {'news': news})
