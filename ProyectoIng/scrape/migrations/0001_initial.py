# Generated by Django 3.0.5 on 2020-04-17 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=20)),
                ('exchange', models.FloatField()),
                ('sign', models.CharField(blank=True, max_length=4, null=True)),
            ],
        ),
    ]
