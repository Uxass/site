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

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')

@admin.register(Articles)

class ArticlesAdmin(admin.ModelAdmin):
    list_filter = ('school_name', 'Hull', 'date')
    fieldsets = (
        (None, {
            'fields': ('title', 'anons', 'full_text',  'genre', 'school_name', 'Hull')
        }),
        ('Корпус и дата', {
            'fields': ('author', 'date')
        }),
    )







