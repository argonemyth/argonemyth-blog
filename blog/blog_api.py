#!/usr/bin/python

# Blog API Python Bindings
# API docs at
# Authors:
# Fei Tan <fei@argonemyth.com>

import requests
import urllib, urllib2
from django.conf import settings

try:
  # Python >= 2.6
  import json as simplejson
except ImportError:
  try:
    # Python < 2.6
    import simplejson
  except ImportError:
    try:
      # Google App Engine
      from django.utils import simplejson
    except ImportError:
      raise ImportError, "Unable to load a json library"

# Configuration variables
API_KEY = settings.API_TOKEN
API_BASE = "http://argonemyth.me/blog/api/"
API_VERSION = None

class BlogAPI(object):
    def __init__(self):
        self.client = requests.Session()

    def _BuildUrl(self, url, path_elements=None, extra_params=None):
        # Break url into constituent parts
        (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(url)

        # Add any additional path elements to the path
        if path_elements:
            # Filter out the path elements that have a value of None
            p = [i for i in path_elements if i]
            if not path.endswith('/'):
                path += '/'
            path += '/'.join(p)

        # Add any additional query parameters to the query string
        if extra_params and len(extra_params) > 0:
            extra_query = self._EncodeParameters(extra_params)
        # Add it to the existing query
        if query:
            query += '&' + extra_query
        else:
            query = extra_query

        # Return the rebuilt URL
        return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))

    def _FetchUrl(self,
                  url,
                  parameters=None,
                  post_data=None,
                  cache=None):
        '''Fetch a URL, optionally caching for a specified time.
        Args:
            url:
                The URL to retrieve
            parameters:
                A dict whose key/value pairs should encoded and added
                to the query string.
            post_data:
                A dict of (str, unicode) key/value pairs.
                If set, POST will be used.
            cache:
                If true, overrides the cache on the current request

        Returns:
            A string containing the body of the response.
        '''
        # Build the custom header for api auth
        headers = {'Authorization': 'Token %s' % API_KEY,
                   'Content-type': 'application/json'}


        # Build the extra parameters dict
        extra_params = {}
        url_params = None
        #print "Going to fetch: " + url
        """
        if self._default_params:
            extra_params.update(self._default_params)
        """
        if parameters:
            extra_params.update(parameters)
            url_params = urllib.urlencode(extra_params)

        if post_data:
            http_method = "POST"
            extra_params.update(post_data)
            url_params = urllib.urlencode(extra_params)
        else:
            http_method = "GET"

        if http_method == "GET" and url_params:
            url += '?' + url_params
        """
            req = urllib2.Request(url, headers)
        else:
            #req = urllib2.Request(url, url_params, headers)
            req = urllib2.Request(url)
        """
        req = urllib2.Request(url, headers)

        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            data = e
        else:
            """
            Some API method (Especially Post methods) returns bad messages as Response Meta data 'Message',
            Get status code if data is None.
            """
            data = response.read()

            if not data:
                #print "Status Code: ", response.getcode()
                if response.getcode() == 201:
                    data = 'Created'
                else:
                    data = None

        return data

    def _send_api_request(self, url, method="get", payload=None):
        headers = {'Authorization': 'Token %s' % API_KEY}
                   # 'Content-type': 'application/json'}

        if payload is None:
            payload = {}

        payload = simplejson.dumps(payload)
        resp = self.client.request(method, url, data=payload,
                                   headers=headers, verify=False)

        if method in ['post'] and resp.status_code != 201:
            # logger.error("Sentry API returned: %s" % resp.content)
            print "API returned: %s" % resp.content
            return None

        if method == ['get', 'put'] and resp.status_code != 200:
            # logger.error("Sentry API returned: %s" % resp.content)
            print "API returned: %s" % resp.content
            return None

        if method == 'delete' and resp.status_code != 204:
            # logger.error("Sentry API returned %s for delete method" % resp.status_code)
            print "API returned: %s" % resp.content
            return False

        try:
            resp_content = simplejson.loads(resp.content)
        except Exception as e:
            if method != 'delete':
                # logger.error("Can't load the json string returned by API: %s" % e)
                print "Can't load the json string returned by API: %s" % e
            else:
                resp_content = True
        # print resp_content
        return resp_content


    def posts(self):
        """Get all the blog post on the remote server.

        Returns:
            A Python list of all the posts:
            [{u'category': u'http://argonemyth.me/blog/api/categories/journey/',
              u'description': u"XXXXXX",
              u'date_expired': None,
              u'title': u'XXXXXXXXXX',
              u'author': u'vivicrow',
              u'id': 11,
              u'content': u'XXXXXXXXX',
              u'date_published': u'2010-08-05T19:00:00Z',
              u'published': True,
              u'slug': u'ile-sainte-marie-and-cetamada',
              u'tags': [],
              u'api_url': u'#/post/ile-sainte-marie-and-cetamada'},...]
        """
        url = API_BASE + 'posts/'
        result = self._send_api_request(url)
        return result

    def get_post_by_url(self, url):
        """
        Get blog post by giving the full api url.

        Returns:
            A dictionary with the detail of the post:
            {u'id': 1,
             u'category': u'http://argonemyth.me/blog/api/categories/dev/',
             u'author': u'vivicrow',
             u'title': u'argonemyth.com Afterthoughts',
             u'slug': u'argonemyth-com-afterthoughts',
             u'description': u'About the development process of argonemyth.com.',
             u'content': u'...',
             u'published': True,
             u'date_published': u'2011-07-04T13:06:19Z',
             u'date_expired': None,
             u'tags': [u'freelance', u'website development', u'argonemyth'],
             u"date_created": "2013-09-08T12:18:20.742Z",
             u"date_updated": "2014-01-18T14:59:41.037Z",
             u'api_url': u'#/post/argonemyth-com-afterthoughts'}
        """
        # result = simplejson.loads(self._FetchUrl(url))
        result = self._send_api_request(url)
        # print result
        return result

    def categories(self):
        """ Get all the blog categories on the remote server.

        Returns:
            A Python list of all the categories:
            [{u'id': 1,
              u'title': u'Dev',
              u'slug': u'dev'
              u'position': 1,
              u'background': u'',
              u'blogposts': [
                  u'http://argonemyth.me/blog/api/posts/a-comprehensive-list-of-insanely-useful-django-apps/',
                  u'http://argonemyth.me/blog/api/posts/daily-linux-command-line-arsenals/',
                  u'http://argonemyth.me/blog/api/posts/argonemyth-com-afterthoughts/'],
              }, ...]
        """
        url = API_BASE + 'categories/'
        result = self._send_api_request(url)
        return result

    def get_category_by_url(self, url):
        """
        Get category by giving the full api url.
        """
        result = self._send_api_request(url)
        # print result
        return result

    def locations(self):
        """ Get all the locations from the remote server.

        Returns:
            A Python list of all the locations:
            [{"id": 1, "latitude": "-20.1619", "longitude": "57.498901",
              "city": "Port Louis", "region": "18", "country": "Mauritius",
              "country_code": "MU"},...]
        """
        url = API_BASE + 'locations/'
        result = self._send_api_request(url)
        return result

    def photos(self):
        """
        Get all the photos from the remote server.
        """
        url = API_BASE + 'photos/'
        result = self._send_api_request(url)
        return result


if __name__ == '__main__':
    blog_api = BlogAPI()
    # posts = blog_api.posts()
    # cats = blog_api.categories()
    # print cats
    post = blog_api.get_post_by_url('http://argonemyth.me/blog/api/posts/argonemyth-com-afterthoughts/')
