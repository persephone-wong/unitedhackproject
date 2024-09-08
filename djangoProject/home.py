import pytz
from django.http import JsonResponse
from django.shortcuts import redirect
import requests
from datetime import datetime
from django.shortcuts import render
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings
import pytz


def get_spotify_playlists(token_info):
    sp = Spotify(auth=token_info['access_token'])
    playlists = sp.current_user_playlists()
    return playlists['items']

def get_greetings():
    now = datetime.now()
    hour = now.hour
    if hour < 12:
        return "Good Morning!"
    elif hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"


def get_weather_category(weather_code):
    if weather_code in [0, 1]:
        return 'sunny'
    elif weather_code in [2, 3]:
        return 'cloudy'
    elif weather_code in [45, 48]:
        return 'foggy'
    elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        return 'rainy'
    elif weather_code in [56, 57, 66, 67]:
        return 'rainy'
    elif weather_code in [71, 73, 75, 85, 86]:
        return 'snowy'
    elif weather_code in [95, 96, 99]:
        return 'thunderstorm'
    else:
        return 'default'

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

    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&timezone=auto'
    response = requests.get(url)
    weather_data = response.json()

    if response.status_code == 200:
        weather_data = response.json()
        current_weather = weather_data.get('current_weather', {})
    else:
        current_weather = {}

    weather_code = current_weather.get('weathercode', None)

    road_work_url = (f'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/'
                     f'road-ahead-upcoming-projects/records?'
                     f'where=within_distance(geo_point_2d,GEOM%27POINT({longitude}%20{latitude})%27,1km)'
                     f'&limit=20')

    road_work_response = requests.get(road_work_url)
    road_work_count = 0

    if road_work_response.status_code == 200:
        road_work = road_work_response.json()
        results = road_work.get('results', [])
        road_work_count = len(results)
    else:
        print("not working")




    # Format the time
    timezone = pytz.timezone(weather_data.get('timezone'))
    raw_time = datetime.now(timezone)
    print(raw_time)
    if raw_time:
        formatted_date = raw_time.strftime('%A, %B %d, %Y')
        formatted_time = raw_time.strftime('%I:%M %p')
    else:
        formatted_time = 'N/A'
        formatted_date = 'N/A'

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


    print(weather_data)
    location = weather_data.get('timezone', 'Unknown').split('/')[-1]
    weather_category = get_weather_category(weather_code)

    context = {
        'greetings': get_greetings(),
        # 'time': weather_data['current_weather']['time'],
        'time': formatted_time,
        'date': formatted_date,
        'location': location,
        'weather': WEATHER_CODE_MAP.get(weather_data['current_weather']['weathercode']) if weather_data else 'N/A',
        'temperature': weather_data['current_weather']['temperature'] if weather_data else 'N/A',
        'emoji': WEATHER_EMOJI_MAP.get(current_weather.get('weathercode', '🌡️')),
        'snow_message': snow_message,
        'snow_delay': snow_delay,
        'rain_delay': rain_delay,
        'work_estimate': '2 hours',
        'road_work': road_work_count,
        'weather_category': weather_category,
        'background_gif': f"{weather_category}.gif"
    }

    token_info = request.session.get('token_info')
    if not token_info:
        context['needs_spotify_sign_in'] = True
    else:
        playlists = get_spotify_playlists(token_info)
        context['playlists'] = playlists

    return render(request, 'home.html', context)
