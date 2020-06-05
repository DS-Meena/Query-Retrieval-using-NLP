"""python_project URL Configuration

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
# from questions import views as quesv
from answer import views as ansv

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', quesv.emp, name='emp'),   # for Just Views
    path('', ansv.index, name='index'),
    # path('', ansv.curr_output, name='curr_output'),
    # path('hello/', views.hello),
]
