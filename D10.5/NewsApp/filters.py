import django.forms
from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from .models import Post, Author



class PostFilter(FilterSet):
    dateCreation = DateFilter(
        lookup_expr='gte',
        widget=django.forms.DateInput(attrs={'type': 'date'})
    )

    title = CharFilter(
        field_name='title',
        label='Заголовок содержит',
        lookup_expr=('icontains'),
    )
    author = ModelChoiceFilter(
        field_name='author',
        label='Автор',
        lookup_expr=('exact'),
        queryset=Author.objects.all()
    )

    class Meta:
       model = Post
       fields = [
       ]