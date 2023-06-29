import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

'''
определили новостную ленту,
создав подкласс класса Feed фреймворка синдицированных новостных лент.

Атрибуты title, link и description соответствуют элементам RSS <title>,
<link> и <description> в указанном порядке.
'''

class LatestPostsFeed(Feed):
    title = '📽 Киноблог Старинского'
    link = reverse_lazy('blog:post_list')
    description = 'Новые записи в 📽 Киноблог Старинского.'

    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)
    
    def item_pubdate(self, item):
        return item.publish
