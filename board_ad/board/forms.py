from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import Ads,Response


class AdsForm(forms.ModelForm):


    class Meta:
        model = Ads
        fields = ['title', 'text', 'category']



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