from django.shortcuts import render, redirect
import requests
import os
from dotenv import load_dotenv
import math
from django.http import JsonResponse
from django.shortcuts import redirect
import requests
from datetime import datetime
from djangoProject.home import home
from djangoProject.functions import get_coordinates , add_trip

def settings(request):
    return render(request, 'settings.html')

def clear_session_view(request):
    request.session.flush()
    return redirect('/')

def traffic(request):
    return render(request, 'traffic.html')

def weather(request):
    return render(request, 'weather.html')

def road_work(request):
    return render(request, 'road_work.html')

def accidents(request):
    return render(request, 'accidents.html')

def home(request):
    return render(request, 'home.html')
