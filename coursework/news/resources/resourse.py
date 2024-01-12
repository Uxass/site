from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from ..models import Articles, Genre, Tag, Author, School, Hull
from import_export.admin import ExportMixin

class ArticlesResource(resources.ModelResource):
    genre = Field(column_name='genre', attribute='genre', widget=ForeignKeyWidget(Genre, 'name'))
    author = Field(column_name='author', attribute='author', widget=ForeignKeyWidget(Author, ('first_name', 'last_name')))
    school_name = Field(column_name='school_name', attribute='school_name', widget=ForeignKeyWidget(School, 'school_name'))
    Hull = Field(column_name='Hull', attribute='Hull', widget=ForeignKeyWidget(Hull, 'Hull_name'))

    class Meta:
        model = Articles
        fields = ('id', 'title', 'anons', 'full_text', 'date', 'genre', 'author', 'school_name', 'Hull',)
        export_order = ('id', 'title', 'anons', 'full_text', 'date', 'genre', 'author', 'school_name', 'Hull',)

    def dehydrate_date(self, obj):
        # Кастомизация значения поля "date"
        return obj.date.strftime('%Y-%m-%d %H:%M')

    def get_export_queryset(self, request):
        # Кастомизация QuerySet для экспорта данных
        qs = super().get_export_queryset(request)
        # Добавить кастомную логику фильтрации или изменения QuerySet
        return qs.filter(some_field='some_value')
