# Generated by Django 3.2.6 on 2022-04-02 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20220403_0124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='url',
        ),
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.CharField(max_length=150, null=True),
        ),
    ]