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


