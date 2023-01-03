# python imports

# django imports
from django.db.models import Q
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
import pdb
# third party imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    status,
    viewsets,
    mixins,
    permissions,
    response,
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

# inner app imports
from catalogue.models import (
 
    product,
    category,
    
)


# local imports
from .serializers import (
    
    BasketSerializer,
    BasketLineSerializer,
    CustomAddProductSerializer,
    ProductSerializer
)
from .pagination import ObjectPagination2x

# oscar imports
from oscar.core.loading import get_class, get_model
from oscar.apps.payment.exceptions import PaymentError
from oscar.apps.basket import signals
from rest_framework import generics

# oscar api imports
from oscarapi.views import (
    basket,
    basic,
)
from oscarapi.basket import operations

from oscarapi.views import checkout as corecheckout
from oscarapi.basket.operations import request_allows_access_to_basket
from oscarapi.signals import oscarapi_post_checkout
from oscarapi.permissions import IsOwner

Order = get_model("order", "Order")
OrderLine = get_model("order", "Line")
OrderNote = get_model('order', 'OrderNote')
EventHandler = get_class('order.processing', 'EventHandler')








class BasketView(basket.BasketView):
    """
    Customised Basket View

    Api for retrieving a user's basket.

    GET:
    Retrieve your basket
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BasketSerializer


class BasketList(basic.BasketList):
    """
    Custom Basket List View
    Retrieve all baskets that belong to the current (authenticated) user.
    """
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BasketSerializer

class BasketDetail(basic.BasketDetail):
    """
    Custom Basket Detail View
    """
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BasketSerializer


class LineList(basket.LineList):
    """
    Api for adding lines to a basket.

    Permission will be checked,
    Regular users may only access their own basket,
    staff users may access any basket.

    GET:
    A list of basket lines.

    POST(basket, line_reference, product, stockrecord,
         quantity, price_currency, price_excl_tax, price_incl_tax):
    Add a line to the basket, example::

        {
            "basket": "http://127.0.0.1:8000/oscarapi/baskets/100/",
            "line_reference": "234_345",
            "product": "http://127.0.0.1:8000/oscarapi/products/209/",
            "quantity": 3,
            "price_currency": "EUR",
            "price_excl_tax": "100.0",
            "price_incl_tax": "121.0"
        }
    """

    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BasketLineSerializer


class BasketLineDetail(basket.BasketLineDetail):
    """
    Only the field `quantity` can be changed in this view.
    All other fields are readonly.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BasketLineSerializer


class AddProductView(basket.AddProductView):
    """
    Add a certain quantity of a product to the basket.

    POST(url, quantity)
    {
        "url": "http://testserver.org/oscarapi/products/209/",
        "quantity": 6
    }

    If you've got some options to configure for the product to add to the
    basket, you should pass the optional ``options`` property:
    {
        "url": "http://testserver.org/oscarapi/products/209/",
        "quantity": 6,
        "options": [{
            "option": "http://testserver.org/oscarapi/options/1/",
            "value": "some value"
        }]
    }
    """
    # permission_classes = (permissions.IsAuthenticated,)
    add_product_serializer_class = CustomAddProductSerializer
    serializer_class = BasketSerializer

    def post(self, request, *args, **kwargs):  # pylint: disable=redefined-builtin
        # pdb.set_trace()
        p_ser = self.add_product_serializer_class(
            data=request.data, context={"request": request}
        )
        if p_ser.is_valid():
            basket = operations.get_basket(request)
            product = p_ser.validated_data["url"]
            quantity = p_ser.validated_data["quantity"]
            options = p_ser.validated_data.get("options", [])

            basket_valid, message = self.validate(basket, product, quantity, options)
            if not basket_valid:
                return Response(
                    {"reason": message}, status=status.HTTP_406_NOT_ACCEPTABLE
                )

            basket.add_product(product, quantity=quantity, options=options)

            signals.basket_addition.send(
                sender=self, product=product, user=request.user, request=request
            )

            operations.apply_offers(request, basket)
            ser = self.serializer_class(basket, context={"request": request})
            response_data = ser.data
            if basket.lines.filter(product=product).exists():
                response_data['current_line_id'] = basket.lines.filter(product=product).first().id
            return Response(response_data)

        return Response({"reason": p_ser.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)





class ProductView(generics.ListAPIView):
    def get(self,request):

        queryset  = product.objects.filter(is_featured = True).filter(structure='parent')
        serializer = ProductSerializer(queryset,many = True).data
        return Response(serializer,status=status.HTTP_200_OK)
