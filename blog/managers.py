from django.db.models import Manager, Q, Sum
from datetime import datetime
from django.conf import settings


class BlogPostManager(Manager):
    """
    Manage blog posts
    """

    def published(self):
        """ 
        For non-staff users, return items with a published status and whose
        publish and expiry dates fall before and after the current date
        when specified.
        """

        """
        if for_user is not None and for_user.is_staff:
            return self.all()
        """

        #return self.filter(Q(published=True), Q(site__id__exact=settings.SITE_ID),
        return self.filter(Q(published=True), 
                           Q(date_published__lte=datetime.now()) | Q(date_published__isnull=True),
                           Q(date_expired__gte=datetime.now()) | Q(date_expired__isnull=True),
                          )

    def get_recent(self):
        total_count = self.published().count()
        if total_count <= settings.RECENT_POSTS_COUNT:
            return self.published()
        else:
            return self.published()[:settings.RECENT_POSTS_COUNT]

    def get_years(self):
        dates = self.published().values_list('date_published')
        year_list = []
        archive_year = []

        for d in dates:
            if d[0].year not in year_list:
                year_list.append( d[0].year )
                posts = self.published().filter(date_published__year=d[0].year).count()
                archive_year.append( (d[0].year, posts) )

        year_list = None
        return archive_year 

    def get_months(self, year):
        dates = self.published().filter(date_published__year=year).values_list('date_published')
        month_list = []
        archive_month = []

        for d in dates:
            if d[0].month not in month_list:
                month_list.append( d[0].month )
                posts = self.published().filter(date_published__year=year).filter(date_published__month=d[0].month).count()
                archive_month.append( (d[0].month, d[0].strftime('%B'), posts) )

        month_list = None
        return archive_month

    def get_top_posts(self, num=10):
        """
        Get most popular posts by view_count & comment_count
        By the default, the top 10 will be showed.
        """
        return self.published().extra( select={'popularity':'view_count + comment_count'}, order_by=('-popularity', ))[:num]

    """
    def published(self, *args, **kwargs):
        return super(BlogPostManager, self).published(*args, **kwargs) \
            .annotate(num_comments=Count("comments")).select_related(depth=1)
    """


class PhotoManager(Manager):
    def get_query_set(self):
        """
        Only signed-in frirends and family can access.
        """
        return super(PhotoManager, self).get_query_set().filter(is_published=True)

    def public(self):
        return self.get_query_set().filter(is_public=True)
