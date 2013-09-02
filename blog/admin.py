from django.contrib import admin

from blog.models import * 

class BlogPostAdmin(admin.ModelAdmin):
    """
    Admin class for blog posts.
    """
    list_display = ('title', 'admin_summery', 'view_count', 'comment_count', 'category', 'published', 'date_published')
    list_editable = ('category', 'published', 'date_published')
    list_filter = ("category", "published")
    search_fields = ("title", "content")
    date_hierarchy = "date_published"
    ordering = ("-date_published", )

    """
    class Media:
        js = ("/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js",
              "/static/blog/js/tinymce_setup.js",)
    """

admin.site.register(BlogPost, BlogPostAdmin)

class BlogCategoryAdmin(admin.ModelAdmin):
    """
    Admin class for blog categories.
    """
    ordering = ("title", )

admin.site.register(BlogCategory, BlogCategoryAdmin)

'''
class ArchiveAdmin(admin.ModelAdmin):
    """
    Admin class for blog categories.
    """
    list_display = ("year", "month", "post_count")
    ordering = ("year", "month")
    list_filter = ("year", "month", "post_count")

admin.site.register(Archive, ArchiveAdmin)
'''
