from django.urls import path,include
from . views import *

urlpatterns = [
    path('',HomepageView.as_view(),name = "home")
]
