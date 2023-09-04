from rest_framework import serializers
from app.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    """
        Article serializer
    """
    author = serializers.CharField(source='created_by.username')
    class Meta:
        model = Article
        fields = ('title', 'body', 'author')