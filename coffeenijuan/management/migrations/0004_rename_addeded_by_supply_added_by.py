# Generated by Django 4.0.2 on 2022-06-07 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_supply_addeded_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supply',
            old_name='addeded_by',
            new_name='added_by',
        ),
    ]