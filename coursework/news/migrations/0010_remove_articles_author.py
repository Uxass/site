# Generated by Django 4.2.2 on 2023-06-27 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_alter_author_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articles',
            name='author',
        ),
    ]
