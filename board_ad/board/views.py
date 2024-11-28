
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from .models import Ads, User, Response
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import AdsForm, ResponseForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from .forms import UserRegistrationForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login


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
    context_object_name = 'ads'
    paginate_by = 10  # количество записеи на странице

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.


class AdsDetail(LoginRequiredMixin, DetailView):
    model = Ads

    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'ads_one.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'ads'


class AdsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_ads',)
    form_class = AdsForm
    model = Ads
    template_name = 'ads_create.html'

    def form_valid(self, form):
        # Получаем пользователя из текущего запроса
        user = self.request.user

        # Устанавливаем пользователя для объявления, если его нет
        form.instance.user = user

        # Проверка на существование объявления с таким же названием
        if Ads.objects.filter(user=user, title=form.cleaned_data['title']).exists():
            messages.error(self.request, "У вас уже есть объявление с таким названием.")
            return self.render_to_response(self.get_context_data(form=form))  # Отображаем форму с ошибкой

        # Если объявления с таким названием нет, сохраняем
        return super().form_valid(form)

    def get_success_url(self):
        # Перенаправление на страницу созданного объявления
        return reverse_lazy('ads_Detail',
                            kwargs={'pk': self.object.pk})  # Перенаправляем на страницу детализированного объявления


class AdsUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = AdsForm
    # fields = ['title', 'text', 'category']  # Поля, которые можно редактировать
    model = Ads
    template_name = 'ads_edit.html'

    def test_func(self):
        # Проверка, является ли текущий пользователь создателем объявления
        ad = self.get_object()
        return ad.user == self.request.user

    def handle_no_permission(self):
        # Обработка случая, если у пользователя нет прав
        raise PermissionDenied("У вас нет прав на редактирование этого объявления")

    def form_valid(self, form):
        post = form.save(commit=False)
        return super().form_valid(form)

    def get_success_url(self):
        # Перенаправление на страницу созданного объявления
        return reverse_lazy('ads_Detail',
                            kwargs={'pk': self.object.pk})  # Перенаправляем на страницу детализированного объявления


class AbsDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ads
    template_name = 'ads_delete.html'
    success_url = reverse_lazy('ads')

    def test_func(self):
        # Проверка, является ли текущий пользователь создателем объявления
        ad = self.get_object()
        return ad.user == self.request.user

    def handle_no_permission(self):
        # Обработка случая, если у пользователя нет прав
        raise PermissionDenied("У вас нет прав на редактирование этого объявления")


def response_create(request, pk):
    # Получаем объект объявления
    ad = get_object_or_404(Ads, pk=pk)

    # Если пользователь не авторизован
    if not request.user.is_authenticated:
        return redirect('login')  # Перенаправляем на страницу авторизации

    # Если форма была отправлена
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            # Создаем отклик
            response = form.save(commit=False)
            response.user = request.user  # Устанавливаем текущего пользователя
            response.ad = ad  # Связываем отклик с конкретным объявлением
            response.save()
            # Отправка email создателю объявления
            subject = f"Новый отклик на ваше объявление: {ad.title}"
            message = f"Пользователь {request.user.username} оставил отклик: {response.text}"
            from_email = 'noreply@mywebsite.com'  # Используйте ваш email адрес
            recipient_list = [ad.user.email]  # Адрес создателя объявления

            # Отправляем email
            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, "Ваш отклик был отправлен успешно!")

            # Перенаправляем на страницу с подробностями объявления
            return redirect('ads_Detail', pk=ad.pk)

    else:
        form = ResponseForm()

    return render(request, 'response_create.html', {'form': form, 'ad': ad})


@login_required
def response(request, pk):
    user = request.user
    return redirect('')
@login_required
def user_ads(request):
    # Получаем все объявления текущего пользователя
    ads = Ads.objects.filter(user=request.user)
    ad = request.GET.get('ad')  # Получаем id объявления из GET-запроса
    if ad:
        ad_id = Ads.objects.filter(id=ad, user=request.user).first()
        responses = ad_id.responses.all() if ad_id else []
        print(ad_id)
    else:
        responses = Response.objects.filter(ad__user=request.user)  # Если 'ad' не указан, получаем все отклики

    return render(request, 'user_ads.html', {'ads': ads, 'responses': responses, 'ad': ad_id if ad else None})

@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ads, id=ad_id, user=request.user)
    ad.delete()  # Удаляем объявление
    return redirect('user_ads')

@login_required
def user_ads_one(request):
    # Получаем все объявления текущего пользователя
    ads = Ads.objects.filter(user=request.user)


    # # Если передан параметр 'ad', фильтруем отклики для этого объявления
    ad = request.GET.get('ad')  # Получаем id объявления из GET-запроса
    if ad:
        ad_id = Ads.objects.filter(id=ad_id, user=request.user).first()
        responses = ad_id.responses.all() if ad_id else []
        print(ad_id)
    else:
        responses = Response.objects.filter(ad__user=request.user)  # Если 'ad' не указан, получаем все отклики

    return render(request, 'user_ads_one.html', {'ads': ads, 'responses': responses, 'ad': ad_id if ad else None})



@login_required
def accept_response(request, ad_id, response_id):
    ad = get_object_or_404(Ads, id=ad_id, user=request.user)
    response = get_object_or_404(Response, id=response_id, ad=ad)

    if not response.accepted:
        response.accepted = True
        response.save()

        # Отправка email пользователю
        subject = "Ваш отклик принят!"
        message = f"Здравствуйте, {response.user.username}!\n\nВаш отклик на объявление '{ad.title}' был принят.\n\nСпасибо за участие!"
        from_email = 'your_email@gmail.com'
        recipient_list = [response.user.email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, "Отклик успешно принят, сообщение отправлено пользователю.")

    return redirect('user_ads')
@login_required
def accept_response_false(request, ad_id, response_id):
    ad = get_object_or_404(Ads, id=ad_id, user=request.user)
    response = get_object_or_404(Response, id=response_id, ad=ad)
    # Обрабатываем принятие отклика (например, помечаем его как принятый)
    response.accepted = False # Добавьте поле "accepted" в модель Response для этого
    response.save()
    return redirect('user_ads')

def register(request):
    if request.user.is_authenticated:  # Если пользователь уже авторизован
        return redirect('ads')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('confirm_registration')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def confirm_registration(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if request.user.profile.confirmation_code == code:
            request.user.is_confirmed = True
            request.user.profile.confirmation_code = None  # Очистка кода после подтверждения
            request.user.save()
            return redirect('ads')  # Перенаправление на домашнюю страницу
        else:
            return render(request, 'registration/confirm_registration.html', {'error': 'Неверный код!'})

    return render(request, 'registration/confirm_registration.html')
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('ads')  # Если пользователь уже вошел

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password,
                            backend='django.contrib.auth.backends.ModelBackend')
        if user is not None:
            login(request, user)
            return redirect('ads')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'registration/login.html')

def custom_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('custom_login')  # Перенаправление на страницу логина