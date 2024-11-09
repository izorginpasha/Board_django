from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Ads, User,Response
from django.contrib.auth.decorators import login_required
# Create your views here.
class AdsList(LoginRequiredMixin, ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Ads
    queryset = Ads.objects.all().order_by('title')


    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'board.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.

class AdsDetail(LoginRequiredMixin, DetailView):
    model = Ads

    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'board.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10
class AdsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Ads
class AbsUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    model = Ads

class AbsDelete(LoginRequiredMixin, DeleteView):
    model = Ads


@login_required
def response(request, pk):
    user = request.user
    return redirect('')