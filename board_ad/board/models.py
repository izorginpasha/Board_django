from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Response(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    text = models.TextField(default="Текст отсутствует")


    def __str__(self):
        return self.text

class Ads(models.Model):

    CATEGORIES = [
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('dd', 'ДД'),
        ('traders', 'Торговцы'),
        ('guild_masters', 'Гилдмастеры'),
        ('Quest Givers', 'КвестГиверы'),
        ('Kuznetsov','Кузнеци'),
        ('Tanners','Кожевники'),
        ('Potion Makers','Зельевары'),
        ('Spell Masters','Мастера заклинаний'),
        # добавьте остальные категории здесь
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=55)
    text = models.TextField(default="Текст отсутствует")
    category = models.CharField(max_length=20, choices=CATEGORIES, default='tanks')
    response = models.ForeignKey(Response, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Create your models here.
