from django.urls import path
from . import views
from .views import export_data_to_excel

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('create', views.create, name='create'),
    path('<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),#С помощью int отслеживаем параметр, целое число под названием pk
    path('export/', export_data_to_excel, name='export_data_to_excel'),
    
]
