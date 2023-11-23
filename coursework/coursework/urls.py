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
        
class ArticlesViewSet(ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

    @action(methods=['GET'], detail=False)
    def latest_news(self, request):
        # Возвращает последние 5 новостей
        latest_news = Articles.objects.order_by('date')[:5]
        serializer = self.get_serializer(latest_news, many=True)
        return Response(serializer.data)


class ArticlesFViewSet(ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

    queryset = Articles.objects.filter(
        Q(genre__exact='1') | #1 - категория учёба
        Q(genre__exact='2') #2 - категория образование
    )                       # Эти Q запросы могут пригодится, т.к. категории похожи, но при этом имеют важные отличия. Например, они могут пригодится, если мы захотим собрать все статьи связанные только с учёбой и образование
                            # Использован __exact из-за связи в БД, т.к. __contains нельзя использовать с некоторыми связанными полями, такими как поле-ключ или поле-множество.
                                
router = routers.DefaultRouter()
router.register(r'Genre', GenreViewSet)
router.register(r'Author', AuthorViewSet)
router.register(r'Articles', ArticlesViewSet)
router.register(r'ArticlesF', ArticlesFViewSet)




urlpatterns = [
    path('api', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('news/', include('news.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

