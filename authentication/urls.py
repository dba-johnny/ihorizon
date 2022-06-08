from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),    
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
]
