from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib import admin
from ckeditor_uploader.fields import RichTextUploadingField


class Ads(models.Model):
    CATEGORIES = [
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('dd', 'ДД'),
        ('traders', 'Торговцы'),
        ('guild_masters', 'Гилдмастеры'),
        ('Quest Givers', 'КвестГиверы'),
        ('Kuznetsov', 'Кузнеци'),
        ('Tanners', 'Кожевники'),
        ('Potion Makers', 'Зельевары'),
        ('Spell Masters', 'Мастера заклинаний'),
        # добавьте остальные категории здесь
    ]
    paginate_by = 10

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=55)
    text = RichTextUploadingField(verbose_name="Контент")  # Поддержка текста, картинок, видео
    category = models.CharField(max_length=20, choices=CATEGORIES, default='tanks')

    def __str__(self):
        return self.title


class Response(models.Model):
    ad = models.ForeignKey(
        Ads,
        on_delete=models.CASCADE,
        related_name='responses',  # Позволяет использовать ad.responses
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text = models.TextField(default="Текст отсутствует")
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания отклика
    accepted = models.BooleanField(default=False)  # Поле для принятия отклика

    def __str__(self):
        return self.text


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f'Профиль пользователя: {self.user.username}'
