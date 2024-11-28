from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import Ads, Response
from django import forms
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ['title', 'text', 'category']
        widgets = {
            'text': CKEditorUploadingWidget(),  # Указываем использование CKEditor
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']  # Только текст отклика


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Генерация кода и сохранение в профиль
            profile = user.profile
            profile.confirmation_code = get_random_string(length=6, allowed_chars='0123456789')
            profile.is_confirmed = False
            profile.save()

            # Отправка письма с кодом
            self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        subject = "Код подтверждения регистрации"
        message = f"Ваш код подтверждения: {user.profile.confirmation_code}"
        from_email = "noreply@yourdomain.com"
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)
