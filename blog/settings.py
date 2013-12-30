from django.conf import settings

RECENT_POSTS_COUNT = getattr(settings, 'BLOGS_RECENT_POSTS_COUNT', 10)
