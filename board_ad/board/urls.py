from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from . import views  # Импортируем views

urlpatterns = [
    # Аутентификация
    path('login/', views.custom_login, name='custom_login'),  # Страница входа
    path('logout/', views.custom_logout, name='custom_logout'),  # Страница выхода
    path('register/', views.register, name='register'),  # Страница регистрации
    path('confirm-registration/', views.confirm_registration, name='confirm_registration'),  # Подтверждение регистрации

    # Объявления
    path('', views.AdsList.as_view(template_name='board.html'), name='ads'),  # Список объявлений
    path('<int:pk>/', views.AdsDetail.as_view(template_name='ads_one.html'), name='ads_detail'),  # Детали объявления
    path('ads/create/', views.AdsCreate.as_view(template_name='ads_create.html'), name='ads_create'),  # Создание объявления
    path('<int:pk>/edit/', views.AdsUpdate.as_view(), name='ads_edit'),  # Редактирование объявления
    path('<int:pk>/delete/', views.AbsDelete.as_view(), name='ads_delete'),  # Удаление объявления

    # Отклики
    path('<int:pk>/response/', views.response_create, name='response_create'),  # Создание отклика
    path('my-ads/', views.user_ads, name='user_ads'),  # Личный кабинет пользователя (список объявлений)
    path('my-ads/<int:ad>/', views.user_ads_one, name='user_ads_one'),  # Детальный просмотр объявления пользователя
    path('delete-ad/<int:ad_id>/', views.delete_ad, name='delete_ad'),  # Удаление объявления пользователем
    path('accept-response/<int:ad_id>/<int:response_id>/', views.accept_response, name='accept_response'),  # Принятие отклика
    path('accept-response-false/<int:ad_id>/<int:response_id>/', views.accept_response_false, name='accept_response_false'),  # Отклонение отклика
]

# Подключение медиафайлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
