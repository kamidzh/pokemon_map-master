# Generated by Django 3.1.14 on 2025-03-23 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0005_pokemon_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='title_en',
            field=models.CharField(default='title en', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pokemon',
            name='title_jp',
            field=models.CharField(default='title jp', max_length=200),
            preserve_default=False,
        ),
    ]
