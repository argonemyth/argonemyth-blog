argonemyth-blog
===============

A blog engine using Django REST Framework.

Getting Started
===============

1. South
Add "South" to your project’s INSTALLED_APPS setting.

Run ./manage.py syncdb


2. Taggit

Add "taggit" to your project’s INSTALLED_APPS setting.

Run ./manage.py syncdb or ./manage.py migrate taggit if using South.

3. Install argonemyth-blog va pip

Add "blog" to your project's INSTALLED_APPS seting.

Run ./manage.py syncdb or ./manage.py migrate blog if using South.

4. Add 'rest_framework' to your INSTALLED_APPS setting.

5. If you're intending to use the browsable API you'll probably also want to add REST framework's login and logout views. Add the following to your root urls.py file.

    urlpatterns = patterns('',
        ...
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    )

6. Add the following to settings.py:

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

7. Django CKEditor
Add ckeditor to your INSTALLED_APPS setting.

Add a CKEDITOR_UPLOAD_PATH setting to the project's settings.py file. This setting specifies an absolute filesystem path to your CKEditor media upload directory. Make sure you have write permissions for the path, i.e.:

    CKEDITOR_UPLOAD_PATH = "/home/media/media.lawrence.com/uploads"

Add CKEditor URL include to your project's urls.py file:

    (r'^ckeditor/', include('ckeditor.urls')),

8 Require easy-thumbnails

https://github.com/SmileyChris/easy-thumbnails

    THUMBNAIL_ALIASES = { 
        "blog.Photo.image": {
            'full': {'size':(930, 620), 'crop': 'scale'},
            'thumbnail': {'size': (40, 40), 'crop': 'smart'}
        }   
    }


8. Addthis

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

9. Geolocation



Settings
========
You can change the following setup in your settings.py if you wish:

* Recent Post Count - by default, it's 10

    BLOGS_RECENT_POSTS_COUNT = 10 
