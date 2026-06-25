from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from .models import Client
from reservations.models import Reservation


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            client = form.save()
            login(request, client, backend='clients.backends.ClientAuthBackend')
            messages.success(request, 'Регистрация успешно завершена!')
            return redirect('clients:profile')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            try:
                client = Client.objects.get(phone=phone)
                if client.check_password(password):
                    login(request, client, backend='clients.backends.ClientAuthBackend')
                    messages.success(request, f'Добро пожаловать, {client.name}!')
                    next_url = request.GET.get('next', 'clients:profile')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Неверный пароль')
            except Client.DoesNotExist:
                messages.error(request, 'Пользователь с таким номером не найден')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('clients:login')


@login_required
def profile_view(request):
    reservations = Reservation.objects.filter(
        client=request.user
    ).order_by('-check_in_date')

    return render(request, 'registration/profile.html', {
        'client': request.user,
        'reservations': reservations,
    })