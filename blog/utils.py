from django.conf import settings

import urllib, urllib2
from urlparse import urljoin
import os


# TODO - will put it in the settings later
DOMAIN = 'http://www.argonemyth.me'

def download_photo(image_src):
    image_url = urljoin(DOMAIN, image_src)
    print "Downloading Image: %s" % image_url 
    image_name = image_src.split("/")[-1]
    file_name = image_name.split('.')
    thumb_name = u"%s_thumb.%s" % (file_name[0], file_name[1])
    thumb_src = image_src.replace(image_name, thumb_name)
    thumb_url = urljoin(DOMAIN, thumb_src)
    print "Downloading Image Thumb: %s" % thumb_url

    outpath = os.path.join(settings.MEDIA_ROOT,
                          image_src.replace('/media/', ''))
    outpath_thumb = os.path.join(settings.MEDIA_ROOT,
                                 thumb_src.replace('/media/', ''))
    # print "Image output path: %s" % outpath
    # print "Image thumb output path: %s" % outpath_thumb
    output_dir = os.path.dirname(outpath)
    if not os.path.exists(output_dir):
        # print "Creating dir: ", output_dir
        os.makedirs(output_dir)
    urllib.urlretrieve(image_url, outpath)
    urllib.urlretrieve(thumb_url, outpath_thumb)