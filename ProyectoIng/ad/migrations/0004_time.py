# Generated by Django 3.0.3 on 2020-05-07 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0003_ad_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(verbose_name='Dias para desabilitar anuncios')),
            ],
        ),
    ]
