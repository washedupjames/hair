# Generated by Django 5.1.4 on 2025-02-20 17:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=250)),
                ('slug', models.SlugField(max_length=250, unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('brand', models.CharField(default='un-branded', max_length=250)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('image', models.ImageField(upload_to='images/')),
                ('order', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='store.category')),
            ],
            options={
                'verbose_name_plural': 'products',
            },
        ),
    ]
