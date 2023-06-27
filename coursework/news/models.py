from django.db import models

# Create your models here.
class Articles(models.Model):
    title = models.CharField('Название', max_length=50)
    anons = models.CharField('Анонс', max_length=50)
    full_text = models.TextField('Статья')
    date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.title #После self. вывод нужные данные с помощью метода str, который позволяет указать как именно будет вызываться каждый отдельный объект"""
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
