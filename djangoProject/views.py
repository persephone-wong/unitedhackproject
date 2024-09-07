from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
import requests

WEATHER_CODE_MAP = {
    0: 'Clear sky',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Overcast',
    45: 'Fog',
    48: 'Depositing rime fog',
    51: 'Drizzle: Light',
    53: 'Drizzle: Moderate',
    55: 'Drizzle: Dense intensity',
    56: 'Freezing Drizzle: Light',
    57: 'Freezing Drizzle: Dense intensity',
    61: 'Rain: Slight',
    63: 'Rain: Moderate',
    65: 'Rain: Heavy intensity',
    66: 'Freezing Rain: Light',
    67: 'Freezing Rain: Heavy intensity',
    71: 'Snow fall: Slight',
    73: 'Snow fall: Moderate',
    75: 'Snow fall: Heavy intensity',
    77: 'Snow grains',
    80: 'Rain showers: Slight',
    81: 'Rain showers: Moderate',
    82: 'Rain showers: Violent',
    85: 'Snow showers: Slight',
    86: 'Snow showers: Heavy',
    95: 'Thunderstorm: Slight or moderate',
    96: 'Thunderstorm with slight hail',
    99: 'Thunderstorm with heavy hail'
}

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
        'weather': WEATHER_CODE_MAP.get(weather_data['current_weather']['weathercode']) if weather_data else 'N/A',
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
