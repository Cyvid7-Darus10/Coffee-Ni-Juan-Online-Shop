# Generated by Django 4.0.2 on 2022-05-27 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='address',
            field=models.CharField(default='None', max_length=30),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_option',
            field=models.CharField(default='None', max_length=30),
        ),
        migrations.AddField(
            model_name='payment',
            name='total',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
