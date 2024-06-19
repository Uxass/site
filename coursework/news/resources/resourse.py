from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from ..models import Articles, Genre, Tag, Author, School, Hull
from import_export.admin import ExportMixin

class ArticlesResource(resources.ModelResource):

    def get_export_queryset(self, request=None):
        # Кастомизированный метод get_export_queryset
        queryset = super().get_export_queryset(request)
        # Дополнительная логика для кастомизации queryset
        return queryset.filter(published=True)  # Пример: фильтрация только опубликованных записей

    def dehydrate_title(self, article):
        # Кастомизированный метод dehydrate_{field_name}
        # Логика для кастомизации экспортируемого поля title
        return article.title.upper()  # Пример: приведение заголовка к верхнему регистру

    def get_author(self, article):
        # Кастомизированный метод get_{field_name}
        # Логика для кастомизации значения поля author
        return "{} {}".format(article.author.first_name, article.author.last_name)  # Пример: объединение имени и фамилии автора

    class Meta:
        model = Articles
        fields = ('title', 'anons', 'full_text', 'date', 'genre', 'author', 'school_name', 'Hull')



# class ArticlesResource(resources.ModelResource):
#     genre = Field(column_name='genre', attribute='genre', widget=ForeignKeyWidget(Genre, 'name'))
#     author = Field(column_name='author', attribute='author', widget=ForeignKeyWidget(Author, ('first_name', 'last_name')))
#     school_name = Field(column_name='school_name', attribute='school_name', widget=ForeignKeyWidget(School, 'school_name'))
#     Hull = Field(column_name='Hull', attribute='Hull', widget=ForeignKeyWidget(Hull, 'Hull_name'))

#     class Meta:
#         model = Articles
#         fields = ('id', 'title', 'anons', 'full_text', 'date', 'genre', 'author', 'school_name', 'Hull',)
#         export_order = ('id', 'title', 'anons', 'full_text', 'date', 'genre', 'author', 'school_name', 'Hull',)

#     def dehydrate_date(self, obj):
#         # Кастомизация значения поля "date"
#         return obj.date.strftime('%Y-%m-%d %H:%M')

#     def get_export_queryset(self, request):
#         # Кастомизация QuerySet для экспорта данных
#         qs = super().get_export_queryset(request)
#         # Добавить кастомную логику фильтрации или изменения QuerySet
#         return qs.filter(some_field='some_value')
