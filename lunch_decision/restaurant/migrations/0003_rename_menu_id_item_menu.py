# Generated by Django 4.2.9 on 2024-05-13 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_menu_date_alter_item_menu_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='menu_id',
            new_name='menu',
        ),
    ]
