from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('user/list/', UserList.as_view(), name='user_list'),
    path('signin/', LoginView.as_view(template_name='accounts/signin.html'), name='signin'),
    path('signout/', LogoutView.as_view(template_name='accounts/signout.html'), name='signout'),
]