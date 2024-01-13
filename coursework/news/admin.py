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
class ArticlesAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_filter = ('school_name', 'Hull', 'date')
    fieldsets = (
        (None, {
            'fields': ('title', 'anons', 'full_text', 'genre', 'school_name', 'Hull')
        }),
        ('Корпус и дата', {
            'fields': ('author', 'date')
        }),
    )
    list_display = ('title', 'author', 'school_name', 'date', 'genre')
    search_fields = ('title', 'author__first_name', 'author__last_name', 'school_name__school_name')
    list_editable = ('date',)
    resource_class = ArticlesResource

# @admin.register(Articles)
# class ArticlesAdmin(ExportActionModelAdmin):
#     resource_class = ArticlesResource



# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('last_name', 'first_name')

# @admin.register(Articles)

# class ArticlesAdmin(admin.ModelAdmin):
#     list_filter = ('school_name', 'Hull', 'date')
#     fieldsets = (
#         (None, {
#             'fields': ('title', 'anons', 'full_text',  'genre', 'school_name', 'Hull')
#         }),
#         ('Корпус и дата', {
#             'fields': ('author', 'date')
#         }),
#     )







