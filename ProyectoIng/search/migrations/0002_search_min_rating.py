# Generated by Django 3.0.5 on 2020-05-13 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='min_rating',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
