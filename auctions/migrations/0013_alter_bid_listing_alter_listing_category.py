# Generated by Django 4.0.2 on 2022-08-22 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_remove_watchlist_id_alter_watchlist_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Toys', 'Toys'), ('Accessorys', 'Accessorys'), ('Appliances', 'Appliances'), ('Organisms', 'Organisms')], max_length=255),
        ),
    ]
