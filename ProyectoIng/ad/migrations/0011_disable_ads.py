# Generated by Django 3.0.3 on 2020-05-07 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0010_delete_disable_ads'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disable_ads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_to', models.IntegerField(verbose_name='Dias Para desabilitar Anuncios')),
            ],
        ),
    ]
