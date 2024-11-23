from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Добро пожаловать!',
            'Спасибо за регистрацию на нашем сайте.',
            'izorgin.pasha@yandex.ru',
            [instance.email],
            fail_silently=False,
        )


@receiver(post_save, sender=User)
def assign_permissions_to_new_user(sender, instance, created, **kwargs):
    if created:
        # Получаем разрешение
        permission = Permission.objects.get(codename='add_ads')  # Например, разрешение для добавления объявления

        # Добавляем разрешение пользователю
        instance.user_permissions.add(permission)
        # Получаем разрешение
        permission = Permission.objects.get(codename='change_ads')  # Например, разрешение для добавления объявления

        # Добавляем разрешение пользователю
        instance.user_permissions.add(permission)
        permission = Permission.objects.get(codename='delete_ads')  # Например, разрешение для добавления объявления

        # Добавляем разрешение пользователю
        instance.user_permissions.add(permission)