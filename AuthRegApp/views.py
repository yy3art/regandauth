from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from AuthRegApp import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

def get_default_menu() -> tuple:
    return (
        {'url': '/', 'text': 'Главная'},
        {'url': '/login/', 'text': 'Авторизация'},
        {'url': '/register/', 'text': 'Регистрация'},
    )

def index_page(request: HttpRequest) -> HttpResponse:
    context = {
        'page_name': 'Главная',
        'menu': get_default_menu()
    }
    return render(request, 'index.html', context)

def registration_page(request: HttpRequest):
    context = {
        'page_name': 'Регистрация',
        'menu': get_default_menu()
    }
    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = User(username=username, password=password, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, f'Вы создали аккаунт {username}')
            return redirect('/')
        else:
            messages.error(request, f'Произошла ошибка')
            return redirect('/register/')
    else:
        form = forms.UserRegistrationForm()
        context['form'] = form
    return render(request, 'registration.html', context)

def login_page(request: HttpRequest):
    context = {'page_name': 'Авторизация', 'menu': get_default_menu()}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        username = form.data.get('username')
        password = form.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Авторизация прошла успешно')
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Неправильный логин или пароль')
            return redirect('/login/')
    else:
        form = forms.LoginForm()
        context['form'] = form
    return render(request, 'login.html', context)

@login_required
def logout_page(request: HttpRequest):
    logout(request)
    messages.add_message(request, messages.INFO, 'Вы вышли из аккаунта')
    return redirect('/')

@login_required
def profile_page(request: HttpRequest):
    context = {'page_name': 'Профиль', 'menu': get_default_menu()}
    return render(request, 'profile.html', context)