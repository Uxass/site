"""
URL configuration for coursework project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from news.models import Author, Articles, Genre, Tag, School, Hull
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
# Serializers define the API representation.
class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']


#Swagger
from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
#Swagger

# ViewSets define the view behavior.
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# Routers provide an easy way of automatically determining the URL conf.
class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']
    def validate(self, data):
        if len(data['name']) < 5:
            raise serializers.ValidationError("Название жанра должно содержать как минимум 5 символов.")
        return data    

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    



class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ['title', 'date', 'anons', 'genre']
        

from rest_framework import viewsets
from rest_framework import filters
from django_filters import rest_framework as django_filters

class ArticlesFViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre__name']
    search_fields = ['title', 'anons', 'full_text']
    ordering_fields = ['published_date', 'author']  # пример возмож полей для сортировки

    def get_queryset(self):
        queryset = self.queryset
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__name=genre)
        return queryset

    @action(detail=False, methods=['get'])
    def latest_news(self, request):
        # Возвращает последние 5 новостей
        latest_news = self.queryset.order_by('-published_date')[:5]
        serializer = self.get_serializer(latest_news, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def filter_articles(self, request):
        genre_filter = request.data.get('genres', [])

        # Perform filtering using AND, OR, and NOT operations
        query = Q()
        for genre in genre_filter:
            if genre.startswith('~'):
                query &= ~Q(genre__name=genre[1:])
            else:
                query |= Q(genre__name=genre)

        filtered_articles = self.queryset.filter(query)
        serializer = self.get_serializer(filtered_articles, many=True)
        return Response(serializer.data)
router = routers.DefaultRouter()
router.register(r'Genre', GenreViewSet)
router.register(r'Author', AuthorViewSet)
router.register(r'Articles', ArticlesFViewSet)

#swagger
schema_view = get_schema_view(
 openapi.Info(
 title="Snippets API",
 default_version='v1',
 description="Test description",
 terms_of_service="https://www.google.com/policies/terms/",
 contact=openapi.Contact(email="contact@snippets.local"),
 license=openapi.License(name="BSD License"),
 ),
 public=True,
 permission_classes=(permissions.AllowAny,),
)
#swagger
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', include('social_django.urls')),
    path('token/', obtain_auth_token), 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
name='schema-swagger-ui'),
    path('api', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('news/', include('news.urls')),
    path('articles/genre/<str:genre>/', ArticlesFViewSet.as_view({'get': 'list'}), name='articles-by-genre'),
    path('articles/', ArticlesFViewSet.as_view({'get': 'list'}), name='articles-list'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)