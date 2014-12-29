from django.conf.urls import url, patterns, include
from django.conf import settings

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import viewsets, routers

from blog.feeds import BlogPostFeed, BlogPostFeedByCategory
from blog import views

"""
# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'categories', BlogCategoryViewSet)

from haystack.query import SearchQuerySet
from haystack.views import search_view_factory

sqs = SearchQuerySet().filter(site_id=settings.SITE_ID)
"""

# Blog Feeds
urlpatterns = patterns('',
    ("^feed/(?P<cat_slug>[\w\-]+)/$", BlogPostFeedByCategory()),
    ("^feed/$", BlogPostFeed()),
    #(r'^search/', include('haystack.urls')),
    #url(r'^search/', search_view_factory(searchqueryset=sqs), name="haystack_search"),
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns += patterns("blog.views",
    #url("^tag/(?P<tag>.*)/$", "blog_post_list", name="blog_post_list_tag"),
    #("^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$", "blog_post_list",
    #url("^author/(?P<username>.*)/$", "blog_post_list",
    #    name="blog_post_list_author"),
    #url("^archive/(?P<year>.*)/$", "blog_post_list",
    #    name="blog_post_list_year"),
    #url("^(?P<slug>[\-\d\w]*)$", "blog_post_detail", name="blog_post_detail"),
    #url("^(?P<slug>[\-\d\w]*)$", "blog_post_detail", name="blog_post_preview"),
    #("^archive/(?P<year>\d{4})/$", "archive_months"),
    #url("^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$", "blog_post_list", name="blog_post_list_month"),
    #url("^category/(?P<category>.*)/$", "blog_post_list", name="blog_post_list_category"),
    #url("^post_comment/(?P<blog_id>\d+)/$", 'blog_post_comment', name="blog_post_comment"),
    # With Rest Framework & Anuglar JS
    url(r'^api/categories/$', views.BlogCategoryList.as_view(), name='blogcategory-list'),
    url(r'^api/categories/(?P<slug>[\w\-]+)/$', views.BlogCategoryDetail.as_view(), name='blogcategory-detail'),
    url(r'^api/posts/$', views.BlogPostList.as_view(), name='blogpost-list'),
    url(r'^api/posts/(?P<slug>[\-\d\w]*)/$', views.BlogPostDetail.as_view(), name="blogpost-detail"),
    url(r'^app/partials/(?P<page>[-\w]+.html)/$', 'angular_views'),
    url(r'^app/$', 'home', name="blog_home"),
    # Noral View
    url(r'^blog/(?P<category>[\w\-]+)/(?P<slug>[\w\-]+)/$', views.BlogPostDetailView.as_view(), name='post-detail-old'),
    url(r'^posts/(?P<slug>[\w\-]+)/$', views.BlogPostDetailView.as_view(), name='post-detail'),
    url(r'^(?P<category>[\w\-]*)$', views.BlogPostListView.as_view(), name='post-list'),
    #url(r'^$', views.BlogPostListView.as_view() , name="post-list"),
)

urlpatterns = format_suffix_patterns(urlpatterns)
