# Generated by Django 5.1.6 on 2025-02-09 16:27

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='articles/')),
                ('title', models.TextField(max_length=100)),
                ('author', models.TextField(default='admin', max_length=20)),
                ('desc', django_ckeditor_5.fields.CKEditor5Field()),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
