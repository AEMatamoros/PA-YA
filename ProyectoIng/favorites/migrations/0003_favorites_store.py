# Generated by Django 3.0.3 on 2020-05-14 04:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0005_auto_20200513_1713'),
        ('favorites', '0002_auto_20200501_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites_Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_favorite_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favoritos_tiendas', to='store.Store')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tienda Favorito',
                'verbose_name_plural': 'Tiendas Favoritos',
            },
        ),
    ]
