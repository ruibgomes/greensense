from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('showresult', views.showresult, name='showresult'),
    path('analyze', views.analyze, name='analyze'),
] 