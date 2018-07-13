"""chain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import include
from index.views import index, login_view, logout, password_update, login_historys

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('', index),
    path('index', index, name="index"),
    path('login', login_view),
    path('logout', logout),
    path('password_update', password_update, name="password_update"),
    path('index/login-history', login_historys, name="login-history"),
    path('asset/', include('asset.urls', namespace="asset", ), ),
    # path('tasks/', include('tasks.urls', namespace="tasks", ), ),
]
