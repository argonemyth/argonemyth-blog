from rest_framework import serializers
from blog.models import BlogPost, BlogCategory


class TagListSerializer(serializers.WritableField):
    """
    Serialize Django Taggit objects
    """
    def from_native(self, data):
        """
        Called when submitting
        """
        if type(data) is not list:
            print data
            try:
                data = data.strip().split(',')
            except:
                raise ParseError("expected a list of data or a comma seperated string")     
        print data
        return data
     
    def to_native(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj


class BlogCategorySerializer(serializers.HyperlinkedModelSerializer):
    api_url = serializers.SerializerMethodField('get_api_url')

    class Meta:
        model = BlogCategory
        fields = ('id', 'title', 'slug', 'position', 'background', 'blogposts')
        read_only_fields = ('id', 'slug')

    def get_api_url(self, obj):
        return "#/category/%s" % obj.slug


class BlogPostSerializer(serializers.ModelSerializer):
    # author = serializers.Field(source='author.username')
    category_id = serializers.Field(source='category.pk')
    author_id = serializers.Field(source='author.pk')
    tags = TagListSerializer(required=False)
    api_url = serializers.SerializerMethodField('get_api_url')

    class Meta:
        model = BlogPost
        fields = ('id', 'category_id', 'author_id', 'title', 'slug', 'description', 'content',
                  'published', 'date_published', 'date_expired', 'tags', 'date_created',
                  'date_updated','api_url')
        read_only_fields = ('id', 'slug')

    def get_api_url(self, obj):
        return "#/post/%s" % obj.slug


