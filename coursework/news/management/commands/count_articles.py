from django.core.management.base import BaseCommand
from news.models import Articles

class Command(BaseCommand):
    help = 'Count the number of articles published on a specific date'

    def add_arguments(self, parser):
        parser.add_argument('date', type=str, help='Дата чтобы подсчитать количество статей (format: YYYY-MM-DD)')

    def handle(self, *args, **kwargs):
        date = kwargs['date']
        article_count = Articles.objects.filter(date__date=date).count()
        self.stdout.write(self.style.SUCCESS(f'Число статей опубликованных {date}: {article_count}'))
