from django.shortcuts import render, redirect
from .models import Password
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, PasswordForm


@login_required(login_url="login")
def bank(request):
    prof = request.user.profile
    passwords = prof.password_set.all()

    context = {
        'prof': prof,
        'passwords': passwords,
    }

    return render(request, "bank/index.html", context)


@login_required(login_url="login")
def change_key(request, pk):
    profile = request.user.profile
    password = profile.password_set.get(id=pk)
    form = PasswordForm(instance=password)

    if request.method == "POST":
        form = PasswordForm(request.POST, instance=password)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш ключ был обновлён")
            return redirect('bank')

    context = {
        'form': form,
        'password': password,
    }
    return render(request, "bank/change_key.html", context)


@login_required(login_url="login")
def delete_key(request, pk):
    profile = request.user.profile
    password = profile.password_set.get(id=pk)

    if request.method == "POST":
        password.delete()
        messages.success(request, "Ваш ключ был удалён")
        return redirect('bank')

    context = {
        'object': password,
    }
    return render(request, "bank/delete_key.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, "Пользователя с таким именем не существует")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('bank')
        else:
            messages.error(request, "Указан неверное имя пользователя или пароль")

    return render(request, "bank/login_register.html")


def logout_user(request):
    logout(request)
    messages.info(request, "Пользователь вышел из системы!")
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "Аккаунт создан!")
            login(request, user)
            return redirect('bank')
        else:
            messages.error(request, "При регистрации возникла ошибка!")

    context = {
        'page': page,
        'form': form,
    }
    return render(request, "bank/login_register.html", context)


@login_required(login_url="login")
def add_key(request):
    form = PasswordForm()

    if request.method == "POST":
        form = PasswordForm(request.POST)
        print(request.user.id)
        if form.is_valid():
            user = form.save(commit=False)
            user.owner = request.user.profile
            user.save()
            return redirect('bank')

    context = {'form': form}
    return render(request, 'bank/add_key.html', context)
