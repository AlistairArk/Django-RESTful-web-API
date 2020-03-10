"""mysite URL Configuration

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

# from rate import views
from rate import views

urlpatterns = [
    path ('admin/', admin.site.urls),
    path ('api/redirect/',  views.apiRedirect),
    path ("api/register",   views.apiRegister),
    path ("api/login",      views.apiLogin),
    path ("api/logout",     views.apiLogout),
    path ("api/list",       views.apiList),
    path ("api/view",       views.apiView),
    path ("api/average",    views.apiAverage),
    path ("api/rate",       views.apiRate)
]
