from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import AdsList, AdsDetail, AdsCreate, AdsUpdate, AbsDelete, response, response_create, user_ads, delete_ad, \
    accept_response_false, accept_response, register, confirm_registration, user_ads_one
from django.views.decorators.cache import cache_page
from . import views  # Импортируем views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

                  path('login/', views.custom_login, name='custom_login'),
                  path('logout/', views.custom_logout, name='custom_logout'),
                  path('register/', register, name='register'),
                  path('confirm-registration/', confirm_registration, name='confirm_registration'),
                  path('', AdsList.as_view(template_name='board.html'),
                       name='ads'),
                  path('<int:pk>', AdsDetail.as_view(template_name='ads_one.html'),
                       name='ads_Detail'),
                  path('ads/create', AdsCreate.as_view(template_name='ads_create.html'),
                       name='ads_Create'),
                  path('<int:pk>/edit', (AdsUpdate.as_view()), name='abs_edit'),
                  path('<int:pk>/delete', (AbsDelete.as_view()), name='abs_delete'),
                  path('<int:pk>/response/', response_create, name='response_create'),
                  path('my-ads/', user_ads, name='user_ads'),  # Страница с объявлениями пользователя
                  path('my-ads/<int:ad>', user_ads_one, name='user_ads_one'),  # Страница с объявлениями пользователя
                  path('delete-ad/<int:ad_id>/', delete_ad, name='delete_ad'),  # Удалить объявление
                  path('accept-response/<int:ad_id>/<int:response_id>/', accept_response, name='accept_response'),
                  path('accept-response-false/<int:ad_id>/<int:response_id>/', accept_response_false,
                       name='accept_response_false'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
