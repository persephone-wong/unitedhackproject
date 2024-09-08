from django.http import JsonResponse
from django.shortcuts import redirect
import requests
from django.conf import settings
from django.shortcuts import render


def road_work(request):
    if 'latitude' not in request.GET or 'longitude' not in request.GET:
        return render(request, 'road_work.html')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    road_work_url = (f'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/'
                     f'road-ahead-upcoming-projects/records?'
                     f'where=within_distance(geo_point_2d,GEOM%27POINT({longitude}%20{latitude})%27,1km)'
                     f'&limit=20')

    road_work_response = requests.get(road_work_url)
    road_work_count = 0

    if road_work_response.status_code == 200:
        road_work_data = road_work_response.json()
        results = road_work_data.get('results', [])
        road_work_count = len(results)
    else:
        print("not working")


    context = {
        'road_work_number': road_work_count,

    }

    return render(request, 'road_work.html', context)
