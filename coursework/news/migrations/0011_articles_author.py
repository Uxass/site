# Generated by Django 4.2.2 on 2023-06-27 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_remove_articles_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.author'),
        ),
    ]
