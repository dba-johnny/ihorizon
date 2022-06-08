from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect

from . import forms


class RegisterView(FormView):
    template_name = "auth/register.html"
    form_class = forms.RegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)


class LoginView(FormView):
    template_name = "auth/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("supportdesk_tickets")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(self.request, user)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
