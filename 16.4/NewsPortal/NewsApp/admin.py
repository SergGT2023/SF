from django.contrib import admin
from .models import Author, Category, Post

from django.contrib import admin
from .models import Post

# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('author', 'title','dateCreation')  # оставляем только имя и цену товара
    list_filter = ('author','dateCreation')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('author','title')  # тут всё очень похоже на фильтры из запросов в базу

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
