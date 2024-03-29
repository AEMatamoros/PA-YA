# Generated by Django 3.0.3 on 2020-05-13 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20200506_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='store_email',
            field=models.EmailField(blank=True, default=None, max_length=100, null=True, verbose_name='Correo electrónico'),
        ),
        migrations.AddField(
            model_name='store',
            name='store_phone_number',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='Número de teléfono'),
        ),
        migrations.AddField(
            model_name='store',
            name='store_website',
            field=models.CharField(blank=True, default=None, max_length=60, null=True, verbose_name='Sitio web'),
        ),
    ]
