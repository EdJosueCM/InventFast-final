from django.urls import path
from application.security.views import auth

app_name = 'security'
urlpatterns = [
    path('signup/', auth.signup, name='signup'),
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
]