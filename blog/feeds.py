from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404

from blog.models import BlogPost, BlogCategory


class BlogPostFeed(Feed):
    title = "Argonemyth >> Blog"
    description = "Blog posts from argonemyth.me"
    link = "/blog/"
    author_name = "Fei Tan"
    author_email = "fei.tan@argoneyth.me"
    author_link = "www.argonemyth.me"

    def items(self):
        return BlogPost.objects.published()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
        return item.date_published


class BlogPostFeedByCategory(Feed):
    """
    Feed by blog by blog category.
    """
    author_name = "Fei Tan"
    author_email = "fei.tan@argoneyth.me"
    author_link = "www.argonemyth.me"

    def get_object(self, request, cat_slug):
        return get_object_or_404(BlogCategory, slug=cat_slug)

    def title(self, obj):
        return "Argonemyth >> Blog >> %s" % obj.title

    def description(self, obj):
        return  obj.description

    def link(self, obj):
        return obj.get_absolute_url()

    def items(self, obj):
        return BlogPost.objects.published().filter(category=obj)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
        return item.date_published
