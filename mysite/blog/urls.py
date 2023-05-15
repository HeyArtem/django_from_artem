from django.urls import path
from . import views


# определяется именное пространство
app_name = 'blog'


urlpatterns = [
    # # все посты на странице
    # path('', views.post_list, name='post_list'),

    # все посты на странице на основе класса (нет обработки исключения)
    path('', views.PostListView.as_view(), name='post_list'),

    # # детальное представление поста по id
    # path('<int:id>/', views.post_detail, name='post_detail'),

    # исполью дату и слаг для URL-адреса 
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),

    # комментирование постов
     path('<int:post_id>/comment/',
          views.post_comment, name='post_comment'),
]

