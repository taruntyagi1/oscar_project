from django.urls import path,include
from . views import *

urlpatterns = [
    path('',HomepageView.as_view(),name = "home"),
    path('product/',productdetail.as_view(),name = 'product')
]
