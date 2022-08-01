# Generated by Django 4.0.2 on 2022-07-29 02:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_watchlist_id_alter_watchlist_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='id',
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
