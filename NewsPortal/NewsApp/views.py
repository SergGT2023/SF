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
from django.shortcuts import render, redirect, get_object_or_404
from .models import News, Article
from .forms import NewsForm, ArticleForm

def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news')
    else:
        form = NewsForm()
    return render(request, 'news_form.html', {'form': form})

def news_edit(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news_form.html', {'form': form})

def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        return redirect('news')
    return render(request, 'news_confirm_delete.html', {'news': news})

def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles')
    else:
        form = ArticleForm()
    return render(request, 'article_form.html', {'form': form})

def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'article_form.html', {'form': form})

def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles')
    return render(request, 'article_confirm_delete.html', {'article': article})
