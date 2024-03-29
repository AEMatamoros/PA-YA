# Generated by Django 3.0.5 on 2020-04-17 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(max_length=50)),
                ('correlative_direction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.Location')),
            ],
            options={
                'verbose_name': 'Ubicación',
                'verbose_name_plural': 'Ubicaciones',
            },
        ),
    ]
