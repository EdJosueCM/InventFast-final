from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomUserForm
from django.contrib.auth import authenticate, login,logout

def inicio(request):
    return render(request, 'core/inicio.html')



