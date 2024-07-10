from django.contrib.auth import login
from django.shortcuts import render, redirect

from authentication import forms
from litrevu import settings


def home(request):
    return render(request, 'review/home.html')