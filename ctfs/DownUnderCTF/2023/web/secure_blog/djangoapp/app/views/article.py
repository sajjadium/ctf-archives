from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.models import Article
from app.serializers import ArticleSerializer

class ArticleView(APIView):
    """
        View for Articles
    """

    def get(self, request: Request, format=None):
        """
            Just return all articles
        """
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request: Request, format=None):
        """
            Query articles
        """
        articles = Article.objects.filter(**request.data)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)