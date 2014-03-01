from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import urllib, urllib2
import re
from optparse import make_option
from django.utils.dateparse import parse_datetime

from blog.models import BlogPost, BlogCategory
from blog.blog_api import BlogAPI
from blog.utils import download_photo

class Command(BaseCommand):

    help = "This command will pull all the changes from the server."

    option_list = BaseCommand.option_list + (
        make_option('--nuke',
            action='store_true',
            dest='nuke',
            default=False,
            help='If nuke is true, we will nuke all the local categories & post.'),
        )

    def handle(self, *args, **options):
        """
        Visit http://argonemyth.me/blog/api/posts/ to see the returned list

        """
        api = BlogAPI()

        # Step 1: if nuke is true remove all the categories.
        if options['nuke']:
            # This will also delete all the posts that are associated
            # with the categories.
            BlogCategory.objects.all().delete() 
            BlogPost.objects.all().delete()

        # Step 2: Add all the categories and posts back
        cats = api.categories()
        for c_json in cats:
            # print c_json
            posts = c_json.pop('blogposts')
            try:
                category = BlogCategory.objects.get(id=c_json["id"]) 
            except BlogCategory.DoesNotExist:
                print "Creating a new category: "
                category = BlogCategory(**c_json)
                category.save()
            else:
                # Check if the local categories are matching the remote ones.
                if c_json['slug'] != category.slug:
                    raise Exception('The Category is not synced.')
                else:
                    current_data = category.__dict__.copy()
                    # We check if there are changes
                    current_data.pop('_state')
                    if current_data == c_json:
                        print "%s is already in sync" % c_json['title']
                    else:
                        print "Updating a existing category:"
                        category.__dict__.update(c_json)
                        category.save()

            # Adding all the posts from the category.
            for p_url in posts:
                p_json = api.get_post_by_url(p_url)
                # p_json['category_id'] = category
                # p_json['author'] = User.objects.get(username=p_json['author'])
                tags = p_json.pop('tags')
                api_url = p_json.pop('api_url')
                # scan post content and grab all the embeded images

                try:
                    post = BlogPost.objects.get(id=p_json["id"]) 
                except BlogPost.DoesNotExist:
                    print "Creating a new post: %s" % p_json['title']
                    post = BlogPost(**p_json)
                    post.save()
                    # Adding tags
                    if tags:
                        print "Adding the following tags to post %s: %s" % (post.title, (', ').join(tags))
                        for tag in tags:
                            post.tags.add(tag)
                else:
                    if p_json['slug'] != post.slug:
                        raise Exception('The post is not synced')
                    else:
                        # We compare date_updated value to see the post needs to update
                        remote_update = parse_datetime(p_json['date_updated'])
                        if remote_update > post.date_updated:
                            print "Never version of post %s on the server, updating..." % (post.title)
                            post.__dict__.update(p_json)
                            post.save()
                        else:
                            print "No need to pull changes from the server" 

                # Download all the images - regardless if they already exist or not
                images = re.findall(r'<img.* src="(?P<img>.*?)"', p_json['content'])
                if images:
                    for img_src in images:
                        download_photo(img_src)



        # posts = api.posts()
        # for post in posts:
        #     print "Post ID: ", post["id"]
        #     #author = User.objects.get(username=post["author"] 
        #     cat_url = post["category"]
        #     if cat_url:
        #         cat_json = api.get_category_by_url(cat_url)
        #         print "Category: ", cat_json["title"]
        #         cat_json.pop("blogposts", None)
        #         try:
        #             category = BlogCategory.objects.get(id=cat_json["id"]) 
        #         except BlogCategory.DoesNotExist:
        #             print "Creating a new category: "
        #             print cat_json
        #             category = BlogCategory(**cat_json)
        #             category.save()
        #         else:
        #             print "Updating a existing category:"
        #             print cat_json
        #             category.__dict__.update(cat_json)
        #             category.save()

        # try:
        #     obj = BlogPost.objects.get(id=post["id"])
        # except BlogPost.DoesNotExist:
        #     obj = BlogPost(**post)
        # obj, created = BlogPost.objects.get_or_create(id=post.id,
        #                 defaults={'author': author,
        #                           'title': post["title"],
        #                           'slug': post["slug"],
