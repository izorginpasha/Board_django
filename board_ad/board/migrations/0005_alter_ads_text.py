# Generated by Django 5.1.2 on 2024-11-23 09:54

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_alter_ads_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Контент'),
        ),
    ]
