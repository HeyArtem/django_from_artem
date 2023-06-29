from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status', 'created']
    # правая панель позволяет фильтровать результаты по полям, включенным в атрибут list_filter
    list_filter = ['status', 'created', 'publish', 'author']

    # строка поиска
    search_fields = ['title', 'body']

    # slug заполняется автоматически (при заполнении поста)
    prepopulated_fields = {'slug': ('title',)}

    # поле author отображается поисковым виджетом (при заполнении поста)
    raw_id_fields = ['author']

    # навигационные ссылки для навигации по иерархии дат
    date_hierarchy = 'publish'

    # по умолчанию упорядочены по столбцам STATUS (Статус) и PUBLISH (Опубликован)
    ordering = ['status', 'publish']



# комментарии
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # list_display = ['name', 'email', 'post', 'created', 'active']
    
    # без Email
    # list_display = ['name', 'post', 'created', 'active']

    # # без Email, замена name на Имя
    list_display = ['Имя', 'post', 'created', 'active']

    list_filter = ['active', 'created', 'updated']
    
    # search_fields = ['name', 'email', 'body']
    
    # без Email
    # search_fields = ['name', 'body']    

    # без Email, замена name на Имя
    search_fields = ['Имя', 'Комментарий']