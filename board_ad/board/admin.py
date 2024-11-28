from django.contrib import admin
from .models import Ads
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

class AdsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category')

    formfield_overrides = {
        RichTextUploadingField: {'widget': CKEditorUploadingWidget()},
    }

admin.site.register(Ads, AdsAdmin)