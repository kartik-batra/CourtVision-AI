from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password-reset/',views.password_reset_request, name='password_reset'),
    path('password-reset/done/',views.password_reset_done, name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',views.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/complete/',views.password_reset_complete, name='password_reset_complete'),
    path('set-language/', views.set_language, name='set_language'),
]
