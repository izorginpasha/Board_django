
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
    form_class = AdsForm  # Убедитесь, что форма правильно связана с моделью Ads
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

    return render(request, 'user_ads.html', {'ads': ads})

@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ads, id=ad_id, user=request.user)
    ad.delete()  # Удаляем объявление
    return redirect('user_ads')




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