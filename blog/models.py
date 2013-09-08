from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import ugettext, ugettext_lazy as _
#from django.db.models.signals import post_save
from django.contrib.comments.signals import comment_was_posted
from django.contrib.comments.moderation import CommentModerator, moderator
from django.template.defaultfilters import slugify, truncatewords_html
from django.utils.timezone import now

#from datetime import datetime
import re
from uuslug import uuslug

from blog.managers import BlogPostManager
from taggit.managers import TaggableManager


class BlogPost(models.Model):
    """
    A blog post.
    """
    #sites = models.ManyToManyField(Site)
    #site = models.ForeignKey(Site, related_name="blogposts", default=1)
    category = models.ForeignKey("BlogCategory", related_name="blogposts",
                                 blank=True, null=True)
    author = models.ForeignKey("auth.User", verbose_name=_("Author"),
                               related_name="blogposts")
    title = models.CharField(max_length=255) 
    slug = models.CharField(max_length=255, unique=True, editable=False)
    description = models.CharField(_('description'), max_length=300,
                                   blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    date_published = models.DateTimeField(_('date published'),
                                          default=now)
    # In case you want a post show at perticular period of time 
    date_expired = models.DateTimeField(_('date expired'), blank=True, null=True)
    # Add one whenever people clicked a link, don't need to be accurate
    # Just to sort for popularity. 
    view_count = models.IntegerField(default=0, editable=False)
    # Add one whenever someone published a post 
    comment_count = models.IntegerField(default=0, editable=False)

    tags = TaggableManager(blank=True)

    # Automatic
    # the actual date when the post is created
    date_created = models.DateTimeField(auto_now_add=True, editable=False) 
    # the last modified date
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    # managers
    #admin_objects = models.Manager()
    objects = BlogPostManager()

    class Meta:
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        ordering = ("-date_published",)
        get_latest_by = 'date_published'

    def __unicode__(self):
        return self.title  

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(BlogPost, self).save(*args, **kwargs)

    def is_editable(self, request):
        """
        Restrict in-line editing to the objects's owner and superusers.
        """
        return request.user.is_superuser or request.user.id == self.author_id

    def admin_summery(self):
        """
        Returns the first paragraph or the firest 100 characters of the content.
        """
        content_without_images = re.sub("<p><img.*?></p>", '', self.content)
        for end in ("</p>", "<br />", "\n", ". "):
            if end in content_without_images:
                summery = content_without_images.split(end)[0] + end
                break
        else:
            summery = truncatewords_html(content_without_images, 100)

        return summery
    admin_summery.allow_tags = True
    admin_summery.short_description = _("Post Summery")

    def add_comment_count(self):
        self.comment_count += 1
        self.save()
                                                                                                                                                
    def add_view_count(self):
        self.view_count += 1
        self.save()

    @models.permalink
    def get_absolute_url(self):
        return ("blog_post_preview", (), {"slug": self.slug})

    def render_tags(self):
        """
        If there is no tag, tags will be an emply list,
        and join() will return an empty string.
        """
        tags = [tag.name for tag in self.tags.all()]
        return ','.join(tags)

class BlogPostModerator(CommentModerator):
    email_notification = True

moderator.register(BlogPost, BlogPostModerator)

class BlogCategory(models.Model):
    """
    A category for grouping blog posts into a series.
    """
    title = models.CharField(max_length=100) 
    slug = models.CharField(max_length=100, editable=False)
    #objects = models.Manager()
    #sites = models.ManyToManyField(Site)
    #on_site = CurrentSiteManager()
    
    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(BlogCategory, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ("blog_post_list_category", (), {"category": self.slug})

def add_comment_count(sender, comment, **kwargs):
    if comment.content_type.model == u'blogpost':
        post = BlogPost.objects.get(pk=comment.object_pk)
        post.add_comment_count()

comment_was_posted.connect(add_comment_count)
