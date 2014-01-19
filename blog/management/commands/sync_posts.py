from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import urllib, urllib2

from blog.models import BlogPost, BlogCategory
from blog.blog_api import BlogAPI


class Command(BaseCommand):

    help = "Sync all posts"

    def handle(self, *args, **options):
        """
        Visit http://argonemyth.me/blog/api/posts/ to see the returned list
        """
        api = BlogAPI()
        posts = api.posts()
        for post in posts:
            print "Post ID: ", post["id"]
            #author = User.objects.get(username=post["author"] 
            cat_url = post["category"]
            if cat_url:
                cat_json = api.get_category_by_url(cat_url)
                print "Category: ", cat_json["title"]
                cat_json.pop("blogposts", None)
                try:
                    category = BlogCategory.objects.get(id=cat_json["id"]) 
                except BlogCategory.DoesNotExist:
                    print "Creating a new category: "
                    print cat_json
                    category = BlogCategory(**cat_json)
                    category.save()
                else:
                    print "Updating a existing category:"
                    print cat_json
                    category.__dict__.update(cat_json)
                    category.save()

                
            """
            try:
                obj = BlogPost.objects.get(id=post["id"])
            except BlogPost.DoesNotExist:
                obj = BlogPost(**post)
            obj, created = BlogPost.objects.get_or_create(id=post.id,
                            defaults={'author': author,
                                      'title': post["title"],
                                      'slug': post["slug"],
            """
