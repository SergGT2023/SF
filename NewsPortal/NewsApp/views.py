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
from django.shortcuts import render
from .models import News

def news_search(request):
    title = request.GET.get('title')
    author = request.GET.get('author')
    date = request.GET.get('date')

    news_list = News.objects.all()

    if title:
        news_list = news_list.filter(title__icontains=title)

    if author:
        news_list = news_list.filter(author__icontains=author)

    if date:
        news_list = news_list.filter(date__gte=date)

    return render(request, 'news_search.html', {'news_list': news_list})
