from django.contrib import admin
from .resources.resourse import ArticlesResource
from .models import Articles
from .models import Genre
from .models import Tag, Author, School, Hull
from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from .models import Articles
from import_export import resources
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Articles
# Register your models here.
#admin.site.register(Articles)
admin.site.register(Genre)
admin.site.register(Tag)
#admin.site.register(Author)
admin.site.register(School)
admin.site.register(Hull)
from import_export.admin import ExportActionModelAdmin


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    search_fields = ('last_name', 'first_name')

@admin.register(Articles)
class ArticlesAdmin(ImportExportModelAdmin):
    resource_class = ArticlesResource











