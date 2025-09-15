from django.shortcuts import render


def bank(request):
    return render(request, "bank/home.html")
