# Generated by Django 5.1.2 on 2024-11-23 09:18

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_alter_response_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='text',
            field=ckeditor.fields.RichTextField(default='<p>текст статьи здесь...</p>'),
        ),
    ]
