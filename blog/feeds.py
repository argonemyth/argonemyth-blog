from django.contrib.syndication.views import Feed
from blog.models import BlogPost

class BlogPostFeed(Feed):
    title = "argonemyth >> blog"
    description = "Blog posts from argonemyth.me"
    link = "/blog/"
    author_name = "Fei Tan"
    author_email = "vivicrow@argoneyth.me"
    author_link = "www.argonemyth.me"

    def items(self):
        return BlogPost.objects.published()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
        return item.date_published
