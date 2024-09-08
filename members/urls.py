"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from djangoProject.views import home
from djangoProject.views import settings
from djangoProject.views import road_work
from djangoProject.views import traffic
from djangoProject.views import weather
from django.urls import path
from djangoProject.spotify.spotify_auth import spotify_auth
from djangoProject.spotify.spotify_view import spotify_callback, spotify_playlist
from djangoProject.views import clear_session_view




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home.html'),
    path('settings/', settings, name='settings'),
    path('road_work', road_work, name='road_work'),
    path('traffic', traffic, name='traffic'),
    path('weather', weather, name='weather'),
    path('traffic', traffic, name='traffic'),
    path('spotify_auth/', spotify_auth, name='spotify_auth'),
    path('spotify_callback/', spotify_callback, name='spotify_callback'),
    path('spotify/', spotify_playlist, name='spotify'),
    path('clear_session/', clear_session_view, name='clear_session'),




]

