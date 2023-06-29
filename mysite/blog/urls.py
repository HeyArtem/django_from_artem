from django.urls import path
from . import views
from .feeds import LatestPostsFeed  


# определяется именное пространство
app_name = 'blog'


urlpatterns = [
    # все посты на странице
    path('', views.post_list, name='post_list'),

#     # все посты на странице на основе класса (нет обработки исключения)
#     path('', views.PostListView.as_view(), name='post_list'),

    # # детальное представление поста по id
    # path('<int:id>/', views.post_detail, name='post_detail'),

    # отображать список постов по тегу
     path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),    

    # исполью дату и слаг для URL-адреса 
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),

    # комментирование постов
     path('<int:post_id>/comment/',
          views.post_comment, name='post_comment'),
    
    # about
     path('about/', views.about,  name='post_about'),

     # СОЗДАНИЕ НОВОСТНЫХ ЛЕНТ
     path('feed/', LatestPostsFeed(), name='post_feed'),

     # ПРЕДСТАВЛЕНИЯ ПОИСКА
     path('search/', views.post_search, name='post_search'),    
]

