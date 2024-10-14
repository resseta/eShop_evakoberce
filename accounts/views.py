from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

from accounts.forms import SignUpForm


class SignUpView(CreateView):
    template_name = 'form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')


@login_required
def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

