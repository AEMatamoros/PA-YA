# Generated by Django 3.0.3 on 2020-03-12 02:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0009_auto_20200311_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
