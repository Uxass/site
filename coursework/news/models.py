from django.db import models
from django.urls import reverse
# Create your models here.
class Articles(models.Model):
    title = models.CharField('Название', max_length=50)
    anons = models.CharField('Анонс', max_length=50)
    full_text = models.TextField('Статья')
    date = models.DateTimeField('Дата публикации')
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    school_name = models.ForeignKey('School', on_delete=models.SET_NULL, null=True)
    Hull = models.ForeignKey('Hull', on_delete=models.SET_NULL, null=True)
    def get_absolute_url(self):
         return reverse('news-detail', args=[(self.id)])


    def __str__(self):
        return self.title #После self. вывод нужные данные с помощью метода str, который позволяет указать как именно будет вызываться каждый отдельный объект"""
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Genre(models.Model):

    name = models.CharField(max_length=200, help_text="Введите категорию")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Tag(models.Model):
    name = models.CharField('Название тега', max_length=20)
    articles = models.ManyToManyField('Articles', related_name='tags')

    def str(self):
        return self.name
    class Meta:
        verbose_name = 'Хэштег'
        verbose_name_plural = 'Хэштеги'

class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.first_name
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
class School(models.Model):
    school_name = models.CharField(max_length=100)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.school_name
    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'

class Hull(models.Model):
    Hull_name = models.CharField(max_length=100)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.Hull_name
    class Meta:
        verbose_name = 'Корпус'
        verbose_name_plural = 'Корпуса'
