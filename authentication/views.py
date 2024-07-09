from django.contrib.auth import login
from django.shortcuts import render, redirect

# Create your views here.
from authentication import forms
from litrevu import settings


def signup(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})


def home(request):
    return render(request, 'authentication/home.html')