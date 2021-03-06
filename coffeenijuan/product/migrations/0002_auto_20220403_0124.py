# Generated by Django 3.2.6 on 2022-04-02 17:24

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='label',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('updated', models.DateTimeField(default=datetime.datetime.now)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'ordering': ['-rating'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('updated', models.DateTimeField(default=datetime.datetime.now)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
