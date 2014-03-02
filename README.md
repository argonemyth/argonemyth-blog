argonemyth-blog
===============

A blog engine using Django REST Framework.

## Dependencies

Right now, the app is rather diffcult to setup, I will simplify the setup process once I think the app is ready for production use, which might take a while due my current availability.

### South

Add *South* to your project’s `INSTALLED_APPS` setting.

Run `./manage.py syncdb`

### MaxMind GeoIP C API

You need to install GeoIP from MaxMind

#### In OpenSuse

    $ sudo zypper install GeoIP

#### In CentoOS

    $ yum install python-GeoIP

### The following django apps will be installed along with *argonemyth-blog*

* Taggit
* Django REST Framework
* Django CKEditor
* [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails)
* uuslug
* [django-ipware](https://github.com/un33k/django-ipware)

## Install & Setup

##### Install *argonemyth-blog* va pip

##### Make sure you have the folowing apps to your project's `INSTALLED_APPS` seting:

    INSTALLED_APPS = ( 
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'south',
        'taggit',
        'rest_framework',
        'ckeditor',
        'easy_thumbnails',
        'disqus',
        'blog'
    )

Run `./manage.py syncdb` or `./manage.py migrate` if using South.

##### Django REST Framework Setup

###### URL
 If you're intending to use the browsable API you'll probably also want to add REST framework's login and logout views. Add the following to your root urls.py file.

    urlpatterns = patterns('',
        ...
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    )

###### Add the following to the `settings.py`:

    # REST Framework configurations
    REST_FRAMEWORK = { 
        # Use hyperlinked styles by default.
        # Only used if the `serializer_class` attribute is not set on a view.
        'DEFAULT_MODEL_SERIALIZER_CLASS':
            'rest_framework.serializers.HyperlinkedModelSerializer',

        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        ]   
    }

##### Django CKEditor Setup

Add a `CKEDITOR_UPLOAD_PATH` setting to the project's `settings.py`. This setting specifies an absolute filesystem path to your CKEditor media upload directory. Make sure you have write permissions for the path, i.e.:

    CKEDITOR_UPLOAD_PATH = "/home/media/media.lawrence.com/uploads"

Add CKEditor URL include to your project's urls.py file:

    (r'^ckeditor/', include('ckeditor.urls')),

##### easy-thumbnails Setup


    THUMBNAIL_ALIASES = { 
        "blog.Photo.image": {
            'full': {'size':(930, 620), 'crop': 'scale'},
            'thumbnail': {'size': (40, 40), 'crop': 'smart'}
        }   
    }

##### Settings for GeoIP

    # Needs the download the following two files
    # GeoLiteCity.dat.gz from http://geolite.maxmind.com/download/geoip/database/
    # GeoIP.dat.gz from http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/
    GEOIP_PATH = PROJECT_DIR + '/geoip/'

Don't forget to download `GeoLiteCity.dat.gz` and `GeoIP.dat.gz` from the links above and *unzip* them in a directory corresponding to what you set `GEOIP_PATH` with in your settings:

    $ gunzip GeoIP.dat.gz
    $ gunzip GeoLiteCity.dat.gz

##### Settings for the app

You can change the following setup in your settings.py if you wish:

* Recent Post Count - by default, it's 10

    BLOGS_RECENT_POSTS_COUNT = 10 

## Optional

##### Addthis

If you wish to customize the content of add this, you will need to create a addthis.html in your base template directory. Below is the default options:

    <!-- AddThis Button BEGIN -->
    <div class="addthis_toolbox addthis_default_style" addthis:title="{{ title }}">
        <a class="addthis_button_preferred_6"></a> {# digg #}
        <a class="addthis_button_preferred_7"></a> {# delicious #}
        <a class="addthis_button_preferred_8"></a> {# stumbleupon #}
        <a class="addthis_button_preferred_2"></a> {# twitter #}
        <a class="addthis_button_preferred_1"></a> {# facebook #}
        <a class="addthis_button_preferred_11"></a> {# myspace #}
        <a class="addthis_button_preferred_4"></a> {# google #}
        <a class="addthis_button_preferred_10"></a> {# email #}
        <a class="addthis_button_preferred_3"></a> {# print #}
        <a class="addthis_button_compact"></a>
        <a class="addthis_button_google_plusone"></a> {# google +1 #}
    </div>  
    <!-- AddThis Button END -->


## Geolocation