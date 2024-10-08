"""
URL configuration for django_and_django_rest_framework project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from djgentelella.urls import urlpatterns as urls_djgentelella

urlpatterns = urls_djgentelella + [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=reverse_lazy('home')), name='home'),
    path('atm/', include(('atm.urls', 'atm'), namespace='atm')),

    path('api-auth/', include('rest_framework.urls')),
    path('holidays/', include(('holidays.urls', 'holidays'), namespace='holidays')),

]
