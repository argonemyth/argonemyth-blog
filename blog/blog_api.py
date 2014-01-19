#!/usr/bin/python

# Blog API Python Bindings
# API docs at 
# Authors:
# Fei Tan <fei@argonemyth.com>

import urllib, urllib2

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
API_KEY = None
API_BASE = "http://argonemyth.me/blog/api/"
API_VERSION = None

class BlogAPI(object):
    def __init__(self):
        self.token = None

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
                  headers=None,
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
            req = urllib2.Request(url, headers)
        else:
            #req = urllib2.Request(url, url_params, headers)
            req = urllib2.Request(url)

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

    def posts(self):
        """
        Get all the blog post on the remote server.
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
        result = simplejson.loads(self._FetchUrl(url))
        return result

    def get_category_by_url(self, url):
        """
        Get category by giving the full api url.
        """
        result = simplejson.loads(self._FetchUrl(url))
        print result
        return result


if __name__ == '__main__':
    blog_api = BlogAPI()
    posts = blog_api.posts()
