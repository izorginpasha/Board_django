from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import AdsList, AdsDetail, AdsCreate, AbsUpdate, AbsDelete, response
from django.views.decorators.cache import cache_page

urlpatterns = [

    path('', AdsList.as_view(template_name='board.html'),
         name='ads'),
    # path('<int:pk>', AdsDetail.as_view(template_name='board.html'),
    #      name='ads_Detail'),
    # path('ads/create', AdsCreate.as_view(template_name='board.html'),
    #      name='ads_Create'),
    # path('ads<int:pk>/edit', cache_page(60 * 5)(AbsUpdate.as_view()), name='abs_edit'),
    # path('ads<int:pk>/delete', cache_page(60 * 5)(AbsDelete.as_view()), name='abs_delete'),
    # path('response/<int:pk>', response, name='response'),

]
