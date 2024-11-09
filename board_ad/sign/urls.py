from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, custom_logout
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('signup/',
         BaseRegisterView.as_view(template_name='registration/signup.html'),
         name='signup'),
    path('logout/', custom_logout, name='custom_logout'),

]


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='premium')
    if not request.user.groups.filter(name='premium').exists():
        premium_group.user_set.add(user)
    return redirect('/')
