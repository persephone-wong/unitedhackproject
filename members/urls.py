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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('settings/', settings, name='settings'),
    path('road_work', road_work, name='road_work'),
    path('traffic', traffic, name='traffic'),
    path('weather', weather, name='weather'),
    path('traffic', traffic, name='traffic')
]

