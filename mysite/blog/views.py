from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
# from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import CommentForm, SearchForm 
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank # представление поиска
from django.contrib.postgres.search import TrigramSimilarity  #Поиск по триграммному сходству


# представления списка опубликованных постов на странице
# def post_list(request):
#     posts = Post.published.all()    
    
#     return render(request,
#                   'blog/post/list.html',
#                   {'posts': posts})


# представления списка опубликованных постов на странице
# c постраничной разбивкой
def post_list(request, tag_slug=None):
    # Постраничная разбивка с 3 постами на страницу
    post_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    # Постраничная разбивка с 3 постами на страницу
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
                  {'posts': posts,
                   'tag': tag})

    




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

    # Схожие посты по тегу
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                    .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                    .order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})


# class PostListView(ListView):
#     '''
#     представление списка постов
#     на основе класса

#     пока у меня написана защита от 404 (если ввести не правильное число
#      страницы или неформатное выражение)
#     '''  
#     queryset = Post.published.all()   
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


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

# about
def about(request):
    context = {"name_page": "about"}

    return render(request, "blog/post/about.html", context=context)


# форма представления для поиска постов
'''
Поле запроса будет использоваться для того, чтобы давать пользователям
возможность вводить поисковые запросы.
Для проверки того, что форма была передана на обработку, в сло-
варе request.GET отыскивается параметр query. Форма отправляется методом
GET, а не методом POST, чтобы результирующий URL-адрес содержал пара-
метр query и им было легко делиться. После передачи формы на обработку
создается ее экземпляр, используя переданные данные GET, и проверяется
валидность данных формы. Если форма валидна, то с по мощью конкретно-
прикладного экземпляра SearchVector, сформированного с использованием
полей title и body, выполняется поиск опубликованных постов.
'''
# def post_search(request):
#     form = SearchForm() # создается экземпляр формы SearchForm
#     query = None
#     results = []

#     # Для проверки того, что форма была передана на обработку, 
#     # в словаре request.GET отыскивается параметр query
#     if 'query' in request.GET:

#         # Форма отправляется методом GET, а не методом POST, чтобы результирующий 
#         # URL-адрес содержал параметр query и им было легко делиться.
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']

#             # search_vector = SearchVector('title', 'body')            
#             # search_query = SearchQuery(query)

#             # # выделяются основы слов и удаляются стоп-слова на испанском языке
#             # search_vector = SearchVector('title', 'body', config='spanish')
#             # search_query = SearchQuery(query, config='spanish')

#             # Взвешивание запросов
#             search_vector = SearchVector('title', weight='A') + \
#                             SearchVector('body', weight='B')
#             search_query = SearchQuery(query)
            

#             # # с по мощью конкретноприкладного экземпляра SearchVector, сформированного 
#             # # с использованием полей title и body, выполняется поиск опубликованных постов.
#             # results = Post.published.annotate(
#             #     search=SearchVector('title', 'body'),
#             #     ).filter(search=query)

#             # results = Post.published.annotate(
#             #     search=search_vector,
#             #     rank=SearchRank(search_vector, search_query)
#             #     ).filter(rank__gte=0.3).order_by('-rank')

#             # Поиск по триграммному сходству 
#             results = Post.published.annotate(
#                 similarity=TrigramSimilarity('title', query),
#             ).filter(similarity__gt=0.1).order_by('-similarity')
                
            
#     return render(request,
#                     'blog/post/search.html',
#                     {'form': form,
#                     'query': query,
#                     'results': results})

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']            
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),                
            ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
