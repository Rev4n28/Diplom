from django.shortcuts import render
from .models import Password


def bank(request):
    psw = Password.objects.all()

    context = {
        'passwords': psw
    }

    return render(request, "bank/index.html", context)


def add_key(request):
    return render(request, "bank/add_key.html")


def change_key(request):
    return render(request, "bank/change_key.html")
