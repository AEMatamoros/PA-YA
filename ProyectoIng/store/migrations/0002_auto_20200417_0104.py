# Generated by Django 3.0.5 on 2020-04-17 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='stor_cover_img',
        ),
        migrations.AddField(
            model_name='store',
            name='store_cover_img',
            field=models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_cover_img', to='images.Image'),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_profile_img',
            field=models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_profile_img', to='images.Image'),
        ),
    ]
