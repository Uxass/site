from django.contrib import admin
from .models import Articles
from .models import Genre
from .models import Tag, Author, School, Hull
# Register your models here.
#admin.site.register(Articles)
admin.site.register(Genre)
admin.site.register(Tag)
#admin.site.register(Author)
admin.site.register(School)
admin.site.register(Hull)

@admin.register(Articles)

class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'school_name', 'date')
    list_filter = ('school_name', 'Hull', 'date')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
