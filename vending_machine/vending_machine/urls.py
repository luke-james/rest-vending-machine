"""vending_machine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

from vending_machine_api.views import index
from vending_machine_api.views import MachineView
from vending_machine_api.views import ChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('init/', MachineView.as_view(), name='init machine'),
    path('change/', ChangeView.as_view(), name='get/deposit change'),
]
