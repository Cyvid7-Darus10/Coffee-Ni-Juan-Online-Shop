# Generated by Django 4.0.2 on 2022-05-27 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]