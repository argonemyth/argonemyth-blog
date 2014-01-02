from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import ugettext, ugettext_lazy as _
#from django.db.models.signals import post_save
from django.contrib.comments.signals import comment_was_posted
from django.contrib.comments.moderation import CommentModerator, moderator
from django.template.defaultfilters import slugify, truncatewords_html
from django.utils.timezone import now
from django.core.urlresolvers import reverse

#from datetime import datetime
import re
from uuslug import uuslug
from easy_thumbnails.fields import ThumbnailerImageField

from blog.managers import BlogPostManager, PhotoManager
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

    def get_absolute_url(self):
        #return ("blog_post_preview", (), {"slug": self.slug})
        #return ("post-detail", (), {"slug": self.slug})
        return reverse('post-detail', args=[self.category.slug, self.slug])

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
    I will use this for the main nav menu as well.
    """
    title = models.CharField(max_length=100) 
    slug = models.CharField(max_length=100, editable=False)
    position = models.PositiveSmallIntegerField(_('Position In the menu'),
                                                null = True, blank=True)
    background = ThumbnailerImageField(upload_to='categories', blank=True, null=True,
                                       help_text="If you want to change the\
                                                  site background.")
    #objects = models.Manager()
    #sites = models.ManyToManyField(Site)
    #on_site = CurrentSiteManager()
    
    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
        ordering = ('position', 'title',)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(BlogCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-list', args=[self.slug])

"""
def add_comment_count(sender, comment, **kwargs):
    if comment.content_type.model == u'blogpost':
        post = BlogPost.objects.get(pk=comment.object_pk)
        post.add_comment_count()

comment_was_posted.connect(add_comment_count)
"""


class Photo(models.Model):
    """
    A photo that might attach to a blog post.
    Which will be in slide show.
    """
    post = models.ForeignKey("BlogPost", related_name="photos")
    image = ThumbnailerImageField(upload_to='photos', blank=True, null=True)
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.CharField(max_length=100, editable=False)
    caption = models.CharField(_('caption'), max_length=300, blank=True, null=True)
    position = models.PositiveSmallIntegerField(_('Position In Gallery'))
    #location = models.ForeignKey(Location, related_name="photos", blank=True, null=True)
    is_public = models.BooleanField(_('is public'), default=True)
    is_published = models.BooleanField(_('is published'), default=True)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    tags = TaggableManager(blank=True)

    admin_objects = models.Manager()
    objects = PhotoManager()

    class Meta:
        ordering = ['post', 'position']
        get_latest_by = 'date_added'
        verbose_name = _("photo")
        verbose_name_plural = _("photos")

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Photo, self).save(*args, **kwargs)

    """
    def get_absolute_url(self):
        return reverse('pl-photo', args=[self.title_slug])
    """

    def get_previous_in_gallery(self, gallery):
        try:
            return self.get_previous_by_date_added(galleries__exact=gallery, is_public=True)
        except Photo.DoesNotExist:
            return None

    def get_next_in_gallery(self, gallery):
        try:
            return self.get_next_by_date_added(galleries__exact=gallery, is_public=True)
        except Photo.DoesNotExist:
            return None

