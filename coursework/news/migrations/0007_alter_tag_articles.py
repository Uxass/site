# Generated by Django 4.2.2 on 2023-06-27 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_alter_genre_name_alter_tag_articles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='articles',
            field=models.ManyToManyField(related_name='tags', to='news.articles'),
        ),
    ]