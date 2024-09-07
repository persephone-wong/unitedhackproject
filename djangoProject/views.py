from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def settings(request):
    return render(request, 'settings.html')


def traffic(request):
    return render(request, 'traffic.html')


def weather(request):
    return render(request, 'weather.html')


def road_work(request):
    return render(request, 'road_work.html')


def accidents(request):
    return render(request, 'accidents.html')

