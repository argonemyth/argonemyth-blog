from django.conf.urls.defaults import *
from django.conf import settings
from blog.feeds import BlogPostFeed

"""
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory

sqs = SearchQuerySet().filter(site_id=settings.SITE_ID)
"""

# Blog Feeds
urlpatterns = patterns('',
    ("^feed/$", BlogPostFeed()),
    #(r'^search/', include('haystack.urls')),
    url(r'^search/', search_view_factory(searchqueryset=sqs), name="haystack_search"),
)

# Blog patterns.
urlpatterns += patterns("blog.views",
    #url("^tag/(?P<tag>.*)/$", "blog_post_list", name="blog_post_list_tag"),
    #("^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$", "blog_post_list",
    #url("^author/(?P<username>.*)/$", "blog_post_list",
    #    name="blog_post_list_author"),
    #url("^archive/(?P<year>.*)/$", "blog_post_list",
    #    name="blog_post_list_year"),
    url("^(?P<slug>[\-\d\w]*)$", "blog_post_detail", name="blog_post_detail"),
    url("^(?P<slug>[\-\d\w]*)$", "blog_post_detail", name="blog_post_preview"),
    ("^archive/(?P<year>\d{4})/$", "archive_months"),
    url("^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$", "blog_post_list", name="blog_post_list_month"),
    url("^category/(?P<category>.*)/$", "blog_post_list", name="blog_post_list_category"),
    url("^post_comment/(?P<blog_id>\d+)/$", 'blog_post_comment', name="blog_post_comment"),
    #url("^$", "blog_post_list", name="blog_post_list"),
)
