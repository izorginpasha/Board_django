from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Ads

@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    list_display = ('title', )
