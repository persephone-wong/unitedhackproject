from django.shortcuts import render, redirect
import requests
import os
from dotenv import load_dotenv
import math

load_dotenv()

def get_coordinates(address):
    api_key = 'tvQlJ37eaxHpLkH08u4vfNbWUKKeZD6Gct9-luWTG8c'
    geocode_url = f'https://geocode.search.hereapi.com/v1/geocode?q={address}&apiKey={api_key}'
    response = requests.get(geocode_url)

    if response.status_code != 200:
        print(f"Error fetching coordinates: {response.status_code}, {response.text}")
        return None
    
    data = response.json()
    location = data.get('items', [{}])[0].get('position', {})
    return location

def add_trip(request):
    here_api_key = 'tvQlJ37eaxHpLkH08u4vfNbWUKKeZD6Gct9-luWTG8c'
    home_address = '5559 Staghorn Place, Vancouver, BC'
    school_address = 'BCIT Downtown Campus, Vancouver, BC'
    
    home_coords = get_coordinates(home_address)
    school_coords = get_coordinates(school_address)

    if not home_coords or not school_coords:
        return render(request, 'add_trip.html', {'error': 'Unable to fetch coordinates'})

    home_lat = home_coords.get('lat')
    home_lon = home_coords.get('lng')
    school_lat = school_coords.get('lat')
    school_lon = school_coords.get('lng')

    if not (home_lat and home_lon and school_lat and school_lon):
        return render(request, 'add_trip.html', {'error': 'Invalid coordinates received'})

    # HERE Routing API URL for car transport
    route_url = (f'https://router.hereapi.com/v8/routes?'
                 f'apiKey={here_api_key}&'
                 f'transportMode=car&'
                 f'origin={home_lat},{home_lon}&'
                 f'destination={school_lat},{school_lon}&'
                 f'return=summary')

    response = requests.get(route_url)
    
    print(f"API Response Status Code: {response.status_code}")
    print(f"API Response: {response.text}")

    if response.status_code == 200:
        data = response.json()
        try:
            # Extract the duration in seconds
            driving_time = data.get('routes', [{}])[0].get('sections', [{}])[0].get('summary', {}).get('duration', 0)
            driving_time_minutes = math.ceil(driving_time / 60)
        except (IndexError, KeyError, TypeError) as e:
            print(f"Error parsing driving time: {e}")
            driving_time_minutes = 0
    else:
        print(f"Error fetching driving time: {response.status_code}, {response.text}")
        driving_time_minutes = 0

    context = {
        'home_address': home_address,
        'school_address': school_address,
        'driving_time': driving_time_minutes
    }
    
    return render(request, 'add_trip.html', context)


def settings(request):
    return render(request, 'settings.html')

def clear_session_view(request):
    request.session.flush()
    return redirect('/') 

def traffic(request):
    return render(request, 'traffic.html')

def weather(request, *args, **kwargs):
    return render(request, 'weather.html')

def road_work(request, *args, **kwargs):
    return render(request, 'road_work.html')

def accidents(request, *args, **kwargs):
    return render(request, 'accidents.html')

def home(request, *args, **kwargs):
    return render(request, 'home.html')
