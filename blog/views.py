from calendar import month_name

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import ListView, DetailView
from rest_framework import generics

from blog.models import BlogPost, BlogCategory
from blog.serializers import BlogPostSerializer, BlogCategorySerializer

class BlogPostList(generics.ListCreateAPIView):
    """
    List all the blog post, and create new post
    """
    model = BlogPost
    serializer_class = BlogPostSerializer
    
    def pre_save(self, obj):
        obj.author = self.request.user
    
    def post_save(self, obj, *args, **kwargs):
        if type(obj.tags) is list:
            # if tags were provided in the request
            saved_obj = self.model.objects.get(pk=obj.pk)
            for tag in obj.tags:
                saved_obj.tags.add(tag.strip())


class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and delete a blog post 
    """
    model = BlogPost
    serializer_class = BlogPostSerializer


class BlogCategoryList(generics.ListCreateAPIView):
    """
    List all the blog categoires
    """
    model = BlogCategory
    serializer_class = BlogCategorySerializer


class BlogCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and delete a category
    """
    model = BlogCategory
    serializer_class = BlogCategorySerializer


def home(request, template_name="blog/blog_index.html"):
    """
    The index for blog
    """
    return render_to_response(template_name,
                              context_instance=RequestContext(request))

def angular_views(request, page):
    """
    Render angular partials 
    """
    template_name = "blog/partials/%s" % page
    return render_to_response(template_name,
                              context_instance=RequestContext(request))


class BlogPostContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(BlogPostContextMixin, self).get_context_data(**kwargs)
        context['recent_posts'] = self.model.objects.get_recent()
        #context['top_posts'] = self.model.objects.get_top_posts()
        context['categories'] = BlogCategory.objects.all()
        cat = self.kwargs.get('category', None)
        if cat:
            context['category'] = BlogCategory.objects.get(title__iexact=cat) 
        else:
            context['category'] = 'home' 
        return context


class BlogPostListView(BlogPostContextMixin, ListView):
    model = BlogPost
    context_object_name = "posts"
    paginated_by = 6

    def get_queryset(self):
        category = self.kwargs.get('category', None)
        print category
        if category:
            return self.model.objects.published().filter(
                    category__slug__iexact = category)
        return self.model.objects.published()


class BlogPostDetailView(BlogPostContextMixin, DetailView):
    model = BlogPost
    context_object_name = "post"


def archive_months(request, year):
    """
    Get the monthly status of posts for a year.
    archives will be a list with tuples in this form: 
        (month_in_digits, month_in_string_format, number_of_post)
    """
    archives = BlogPost.objects.get_months(year)

    return render_to_response("blog/argonemyth_archive_months.html", {"archives_month":archives, "year":year}, RequestContext(request))

def blog_post_list(request, tag=None, year=None, month=None, category=None):
    """
    Display a list of blog posts.
    """
    blog_posts = BlogPost.objects.published()
    """
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        blog_posts = blog_posts.filter(keywords=tag)
    if category is not None:
        category = get_object_or_404(BlogCategory, slug=category)
        blog_posts = blog_posts.filter(category=category)
    blog_posts = paginate(blog_posts, request.GET.get("page", 1),
        settings.BLOG_POST_PER_PAGE,
        settings.BLOG_POST_MAX_PAGING_LINKS)
    """
    if year is not None:
        blog_posts = blog_posts.filter(date_published__year=year)
        if month is not None:
            blog_posts = blog_posts.filter(date_published__month=month)
            month = month_name[int(month)]

    if category is not None:
        blog_posts = blog_posts.filter(category__slug=category)

    context = {"blog_posts": blog_posts, "year": year, "month": month,
               "tag": tag, "category": category, }
    return render_to_response("blog/argonemyth_bloglist.html", context, RequestContext(request))

def latest_blog_post(request, template="blog/argonemyth_blog.html"):
    """
    Display the latest blog post - home of blog section
    """
    blog_post = BlogPost.objects.published(for_user=request.user).latest()


def blog_post_detail(request, slug=None, template="blog/blog_post_detail.html"):
    """
    Display a blog post.
    """
    # Create two comment forms - one with posted data and errors that will be
    # matched to the form submitted via comment_id, and an empty one for all
    # other instances.
    """
    commenter_cookie_prefix = "argonemyth-blog-"
    commenter_cookie_fields = ("name", "email", "website")
    comment_data = {}
    for f in commenter_cookie_fields:
        comment_data[f] = request.COOKIES.get(commenter_cookie_prefix + f, "")
    """

    # This allows me to preview of the the post that's not published
    if request.user.is_superuser:
        blog_posts = BlogPost.objects.all()
    else:
        blog_posts = BlogPost.objects.published()

    recent_posts = BlogPost.objects.get_recent();
    top_posts = BlogPost.objects.get_top_posts();

    if slug:
        blog_post = get_object_or_404(blog_posts, slug=slug)
        if blog_post.published:
            blog_post.add_view_count()
    else:
        blog_post = blog_posts.latest() 

    archive = BlogPost.objects.get_years()
    
    # Get Categories
    cats = BlogCategory.objects.filter(blogposts__in=blog_posts).distinct()
    """
    posted_comment_form = CommentForm(request.POST or None, 
                                      initial=comment_data)
    unposted_comment_form = CommentForm(initial=comment_data)
    if request.method == "POST" and posted_comment_form.is_valid():
        comment = posted_comment_form.save(commit=False)
        comment.blog_post = blog_post
        comment.by_author = (request.user == blog_post.user and
                             request.user.is_authenticated)
        comment.ip_address = request.META.get("HTTP_X_FORWARDED_FOR",
                                              request.META["REMOTE_ADDR"])
        comment.replied_to_id = request.POST.get("replied_to")
        comment.save()
        response = HttpResponseRedirect(comment.get_absolute_url())
        # Store commenter's details in a cookie for 90 days.
        cookie_expires = 60 * 60 * 24 * 90
        for f in commenter_cookie_fields:
            cookie_name = commenter_cookie_prefix + f
            cookie_value = request.POST.get(f, "")
            set_cookie(response, cookie_name, cookie_value, cookie_expires)
        return response
    settings.use_editable()
    context = {"blog_post": blog_post, "blog_page": blog_page(),
               "use_disqus": bool(settings.COMMENTS_DISQUS_SHORTNAME),
               "posted_comment_form": posted_comment_form,
               "unposted_comment_form": unposted_comment_form}
    request_context = RequestContext(request, context)
    t = select_template(["blog/%s.html" % slug, template], request_context)
    return HttpResponse(t.render(request_context))
    """
    context = {"blog_post": blog_post, 
               "recent_posts": recent_posts,
               "archive": archive,
               "top_posts": top_posts,
               "categoris": cats,
              }
    return render_to_response("blog/argonemyth_blog.html", context, RequestContext(request))

def blog_post_comment(request, blog_id=None):
    blog_post = get_object_or_404(BlogPost.objects.all(), id=blog_id)
    context = { "blog_post": blog_post }
    return render_to_response("blog/argonemyth_comment_form.html", context, RequestContext(request))
