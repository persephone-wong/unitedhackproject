from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
import requests

def home(request):
    if 'latitude' not in request.GET or 'longitude' not in request.GET:
        return render(request, 'home.html')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    print(latitude, longitude)
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'
    response = requests.get(url)
    weather_data = response.json()
    print(weather_data)

    context = {
        'greetings': 'Welcome!',
        'time': weather_data['current_weather']['time'],
        'date': '2023-10-01',
        'location': weather_data['timezone'] if weather_data else 'Unknown',
        'weather': weather_data['current_weather']['weathercode'] if weather_data else 'N/A',
        'temperature': weather_data['current_weather']['temperature'] if weather_data else 'N/A',
        'work_estimate': '2 hours',
        'playlist': 'Top Hits'
    }

    return render(request, 'home.html', context)


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
