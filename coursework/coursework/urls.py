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

# ViewSets define the view behavior.
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# Routers provide an easy way of automatically determining the URL conf.
class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer



class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ['title', 'date', 'anons', 'genre']
    def validate_title(self, value):
        # Проверка что длинна статьи больше 5 символов
        if len(value) < 5:
            raise serializers.ValidationError("Название статьи должно содержать как минимум 5 символов.")
        return value        
        
class ArticlesFViewSet(ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

    @action(methods=['GET'], detail=False)
    def latest_news(self, request):
        # Возвращает последние 5 новостей
        latest_news = self.queryset.order_by('-date')[:5]
        serializer = self.get_serializer(latest_news, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def filter_articles(self, request, pk=None):
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
#У меня естьfilter_articlesдействие, которое принимает список жанров в POSTтеле запроса. Затем он создает набор запросов, используя операции AND, OR и NOT.
#Объект Qиспользуется для построения запроса на основе входных жанров, реализуя
#The ~используется для обозначения операции НЕ, и код строит запрос соответствующим образом.
#Когда filter_articlesдействие вызывается с POSTзапросом, оно обрабатывает жанровые фильтры и возвращает
# latest_news: HTTP метод GET, которое возвращает последние 5 новостей из queryset, отсортированных по дате.
#filter_articles: HTTP метод POST, которое выполняет фильтрацию статей на основе переданных в запросе жанров. Фильтрация выполняется с использованием операций AND, OR и NOT.
#Для действия filter_articles извлекаются жанры из данных запроса, затем формируется объект запроса query, который используется для фильтрации объектов queryset на основе переданных жанров. Результат фильтрации сериализуется и возвращается в ответе.

#Фильтрация по аргументам именованного URL
class ArticlesFViewSet(ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

    def get_queryset(self):
        genre = self.kwargs.get('genre')  #  Если предположить, что шаблон URL включает жанр в качестве именованного аргумента
        if genre:
            return self.queryset.filter(genre__name=genre)
        return self.queryset


# Фильтрация по параметрам GET в URL-адресе
class ArticlesFViewSet(ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genre__name']


#Фильтрация по поискуSearchFilterпредоставленный Django Rest Framework
class ArticlesFViewSet(ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'anons', 'full_text']  # Поля для поиска

    def get_queryset(self):
        queryset = self.queryset
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(anons__icontains=query) |
                Q(full_text__icontains=query)
            )
        return queryset

router = routers.DefaultRouter()
router.register(r'Genre', GenreViewSet)
router.register(r'Author', AuthorViewSet)
router.register(r'Articles', ArticlesFViewSet)
router.register(r'ArticlesF', ArticlesFViewSet)




urlpatterns = [
    path('api', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('news/', include('news.urls')),
    path('articles/genre/<str:genre>/', ArticlesFViewSet.as_view({'get': 'list'}), name='articles-by-genre'),
    path('articles/', ArticlesFViewSet.as_view({'get': 'list'}), name='articles-list'),
    path('articles/', ArticlesFViewSet.as_view({'get': 'list'}), name='articles-list'),    
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

