"""Helphen_India URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from .views import events, rxd, pp, work, team, home_contact_form
from Kinder.views import kinder_contact_form

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_contact_form, name='home'),
    path('helphen/events/', events, name='events'),
    path('helphen/rxd/', rxd, name='rxd'),
    path('helphen/pp/', pp, name='pp'),
    path('helphen/pk/', kinder_contact_form, name='pk'),
    path('helphen/work/', work, name='work'),
    path('helphen/team/', team, name='team'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
