from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager



'''
Набирай сайт по книге
'''

# конкретно-прикладной менеджер для модели Post, возвращает опубликованные посты 
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
        .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)   
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')    
    body = models.TextField()       
    publish = models.DateTimeField(default=timezone.now)    
    created = models.DateTimeField(auto_now_add=True)    
    updated = models.DateTimeField(auto_now=True) 
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
        
    objects = models.Manager() # менеджер, применяемый по умолчанию
    published = PublishedManager() # конкретно-прикладной менеджер
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']


    indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    
    # # Использование канонических URL-адресов
    # def get_absolute_url(self):
    #     return reverse('blog:post_detail',
    #                    args=[self.id])


    # исполью дату и слаг для URL-адреса 
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
    

# комментирование постов (Убрать маил)
class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    # name = models.CharField(max_length=80)

    # замена name на Имя
    Имя = models.CharField(max_length=80)
    # email = models.EmailField()
    # body = models.TextField()
    Комментарий = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f"Comment by {self.Имя} on {self.post}"
