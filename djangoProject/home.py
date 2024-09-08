
from django.http import JsonResponse
from django.shortcuts import redirect
import requests
from datetime import datetime
from django.shortcuts import render
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings


def get_spotify_playlists(token_info):
    sp = Spotify(auth=token_info['access_token'])
    playlists = sp.current_user_playlists()
    return playlists['items']


def home(request):

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

    WEATHER_EMOJI_MAP = {
        0: '☀️',  # Clear sky
        1: '🌤️',  # Mainly clear
        2: '⛅',  # Partly cloudy
        3: '☁️',  # Overcast
        45: '🌫️',  # Fog
        48: '🌫️',  # Depositing rime fog
        51: '🌦️',  # Drizzle: Light
        53: '🌧️',  # Drizzle: Moderate
        55: '🌧️',  # Drizzle: Dense intensity
        56: '🌧️❄️',  # Freezing Drizzle: Light
        57: '🌧️❄️',  # Freezing Drizzle: Dense intensity
        61: '🌧️',  # Rain: Slight
        63: '🌧️',  # Rain: Moderate
        65: '🌧️',  # Rain: Heavy intensity
        66: '🌧️❄️',  # Freezing Rain: Light
        67: '🌧️❄️',  # Freezing Rain: Heavy intensity
        71: '❄️',  # Snow fall: Slight
        73: '❄️',  # Snow fall: Moderate
        75: '❄️',  # Snow fall: Heavy intensity
        77: '🌨️',  # Snow grains
        80: '🌦️',  # Rain showers: Slight
        81: '🌦️',  # Rain showers: Moderate
        82: '⛈️',  # Rain showers: Violent
        85: '🌨️',  # Snow showers: Slight
        86: '🌨️',  # Snow showers: Heavy
        95: '⛈️',  # Thunderstorm: Slight or moderate
        96: '⛈️',  # Thunderstorm with slight hail
        99: '⛈️',  # Thunderstorm with heavy hail
    }

    if 'latitude' not in request.GET or 'longitude' not in request.GET:
        return render(request, 'home.html')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'
    response = requests.get(url)
    weather_data = response.json()


    if response.status_code == 200:
        weather_data = response.json()
        current_weather = weather_data.get('current_weather', {})
    else:
        current_weather = {}

    weather_code = current_weather.get('weathercode', None)

    # Format the time
    raw_time = current_weather.get('time')
    if raw_time:
        try:
            # Try parsing the time with 'Z' format
            time_obj = datetime.strptime(raw_time, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            # If that fails, try parsing without 'Z'
            time_obj = datetime.strptime(raw_time, '%Y-%m-%dT%H:%M')

        # Reformat the time into a more readable format
        formatted_time = time_obj.strftime('%B %d, %Y, %I:%M %p')
    else:
        formatted_time = 'N/A'

    # display message if snow or freezing rain in forecast
    snow_message = None
    # display the delay as %
    # TODO: express it as percent of calculated trip time
    rain_delay = None
    snow_delay = None

    if weather_code in [73, 75, 86]:
        snow_message = "Better have winter tires!"
    if weather_code in [67, 71, 73, 75, 86]:
        snow_delay = 50
    if weather_code in [99, 65, 67]:
        rain_delay = 15



    context = {
        'greetings': 'Welcome!',
        # 'time': weather_data['current_weather']['time'],
        'time': formatted_time,
        'date': '2023-10-01',
        'location': weather_data['timezone'] if weather_data else 'Unknown',
        'weather': WEATHER_CODE_MAP.get(weather_data['current_weather']['weathercode']) if weather_data else 'N/A',
        'temperature': weather_data['current_weather']['temperature'] if weather_data else 'N/A',
        'emoji': WEATHER_EMOJI_MAP.get(current_weather.get('weathercode', '🌡️')),
        'snow_message': snow_message,
        'snow_delay': snow_delay,
        'rain_delay': rain_delay,
        'work_estimate': '2 hours',
    }

    token_info = request.session.get('token_info')
    if not token_info:
        context['needs_spotify_sign_in'] = True
    else:
        playlists = get_spotify_playlists(token_info)
        context['playlists'] = playlists
    print(context)
    return render(request, 'home.html', context)
