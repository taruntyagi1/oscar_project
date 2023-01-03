# django imports
from django.urls import path, include

# third party imports
from rest_framework.urlpatterns import (
    format_suffix_patterns,
)
from rest_framework import routers

# inner app imports
from .views import (
   
    BasketView,
    BasketList,
    BasketDetail,
    LineList,
    BasketLineDetail,
    AddProductView,
    ProductView
  
)

router = routers.SimpleRouter(trailing_slash=False)



urlpatterns = [ 

    path("basket/", BasketView.as_view(), name="api-catalogue-basket"),
    path("baskets/", BasketList.as_view(), name="basket-list"),
    path("baskets/<int:pk>/", BasketDetail.as_view(), name="basket-detail"),
    path("baskets/<int:pk>/lines/", LineList.as_view(), name="basket-lines-list"),
    path("baskets/<int:basket_pk>/lines/<int:pk>/", BasketLineDetail.as_view(), name="basket-line-detail",),
    path("basket/add-product/", AddProductView.as_view(), name="basket-add-product"),
    path('product-view/',ProductView.as_view(),name='product-view')
]


# adding router urls
urlpatterns += router.urls

# Add Multiple Format Support
urlpatterns = format_suffix_patterns(urlpatterns)