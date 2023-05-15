from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
# from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import CommentForm
from django.views.decorators.http import require_POST


# представления списка опубликованных постов на странице
# def post_list(request):
#     posts = Post.published.all()    
    
#     return render(request,
#                   'blog/post/list.html',
#                   {'posts': posts})


# представления списка опубликованных постов на странице
# c постраничной разбивкой
def post_list(request):
    # Постраничная разбивка с 3 постами на страницу
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    # содержит запрошенный номер страницы.
    # Если параметра page нет в GET-параметрах запроса, 
    # то мы используем стандартное значение 1, 
    # чтобы загрузить первую страницу результатов.
    page_number = request.GET.get('page', 1)

    # обработка ошибки с несуществующей ошибкой
    try:
        posts = paginator.page(page_number)

    # Если page_number не целое число, то
    # выдать первую страницу
    except PageNotAnInteger:
        posts = paginator.page(1)
    
    # Если page_number находится вне диапазона, то
    # выдать последнюю страницу
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})

    




# # Детальное представление одиночного поста . Открыть пост по id
# def post_detail(request, id):
#     # try:
#     #     post = Post.published.get(id=id)


#     # # исключение Http404, чтобы вернуть ошибку HTTP с кодом 
#     # # состояния, равным 404, если возникает исключение DoesNotExist, 
#     # # то есть модель не существует, поскольку результат не найден.
#     # except Post.DoesNotExist:
#     #     raise Http404("No post found.")        
    
#     # функцию сокращенного доступа для вызова метода get() 
#     # и вызова исключения Http404 когда объект не найден
#     post = get_object_or_404(Post,
#                              id=id,
#                              status=Post.Status.PUBLISHED)
    
   

# Детальное представление поста. Исполью дату и слаг для URL-адреса 
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
     # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)

    # Форма для комментирования пользователями
    form = CommentForm()

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})


class PostListView(ListView):
    '''
    представление списка постов
    на основе класса

    пока у меня написана защита от 404 (если ввести не правильное число
     страницы или неформатное выражение)
    '''  
    queryset = Post.published.all()   
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# комментирование постов
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id, 
                             status=Post.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})