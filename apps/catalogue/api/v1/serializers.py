# third-party imports
from rest_framework import serializers

# inter-app imports
from catalogue.models import (
    DietitionsAndNutritionists,
    product,
    Category,
    BannerImages,
    Option,
    Questionaire,
    Product
)
from basket.models import Basket


# oscar imports
from oscarapi.serializers import basket as corebasket
from oscarapi.serializers import checkout as corecheckout
from oscarapi.serializers.fields import (
    DrillDownHyperlinkedIdentityField,
    DrillDownHyperlinkedRelatedField,
)
from oscar.core.loading import get_class, get_model

# django imports
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()





class BasketSerializer(corebasket.BasketSerializer):
    """
    customised basket serializer
    """
    owner = serializers.HyperlinkedRelatedField(
        view_name="customer:custom_user-detail",
        required=False,
        allow_null=True,
        queryset=User.objects.all(),
    )

    lines = serializers.HyperlinkedIdentityField(view_name="catalogue:basket-lines-list")

    url = serializers.HyperlinkedIdentityField(
        view_name='catalogue:basket-detail',
    )

    class Meta(corebasket.BasketSerializer.Meta):
        fields = (
            "id",
            "owner",
            "status",
            "lines",
            "url",
            "total_excl_tax",
            "total_excl_tax_excl_discounts",
            "total_incl_tax",
            "total_incl_tax_excl_discounts",
            "total_tax",
            "currency",
            "voucher_discounts",
            "offer_discounts",
            "is_tax_known",
        )


class BasketLineSerializer(corebasket.BasketLineSerializer):
    """
    Customised basket line serializer
    """

    url = DrillDownHyperlinkedIdentityField(
        view_name="catalogue:basket-line-detail", extra_url_kwargs={"basket_pk": "basket.id"}
    )

    product = serializers.HyperlinkedRelatedField(
        view_name="catalogue:product_detail",
        required=False,
        allow_null=True,
        queryset=Product.objects.all(),
    )

    basket = serializers.HyperlinkedIdentityField(
        view_name='catalogue:basket-detail',
    )

    product_detail = serializers.SerializerMethodField(read_only=True)

    class Meta(corebasket.BasketLineSerializer.Meta):
        fields = (
            "url",
            "product",
            "quantity",
            "attributes",
            "price_currency",
            "price_excl_tax",
            "price_incl_tax",
            "price_incl_tax_excl_discounts",
            "price_excl_tax_excl_discounts",
            "is_tax_known",
            "warning",
            "basket",
            # "stockrecord",
            "date_created",
            "date_updated",
            "product_detail",
        )

    def get_product_detail(self, obj):
        if obj.product:
            product_image = obj.product.primary_image()
            if hasattr(product_image, 'original'):
                image = product_image.original.url
            else:
                image = None
            data = {
                'title': obj.product.title,
                'description': obj.product.description,
                'image': image,
            }
            
            if obj.product.has_stockrecords:
                selling_price = obj.product.stockrecords.first().price_excl_tax
                retail_price = obj.product.stockrecords.first().price_retail
                data['selling_price'] = selling_price
                data['retail_price'] = retail_price
            image_list = obj.product.get_all_images()
            images_list = []
            for obj in image_list:
                image_dict = {
                    'image': obj.original.url,
                    'caption': obj.caption,
                    'display_order': obj.display_order,
                }
                images_list.append(image_dict)
            if len(images_list) > 0:
                data['images_list'] = images_list
            return data
        return None


class OptionValueSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    option = serializers.HyperlinkedRelatedField(
        view_name="option-detail", queryset=Option.objects
    )
    value = serializers.CharField()


class CustomAddProductSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializes and validates an add to basket request.
    """

    quantity = serializers.IntegerField(required=True)
    # url = serializers.HyperlinkedRelatedField(
    #     view_name="catalogue:product_detail", queryset=Product.objects, required=True
    # )
    # options = OptionValueSerializer(many=True, required=False)
    quantity = serializers.IntegerField(required=True)
    url = serializers.HyperlinkedRelatedField(
        view_name="product-detail", queryset=Product.objects, required=True
    )
    options = OptionValueSerializer(many=True, required=False) 


class ProductListSerializer(serializers.ModelSerializer):
    """
    serializer for blog list
    """

    image = serializers.SerializerMethodField()
    selling_price = serializers.SerializerMethodField()
    retail_price = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    image_list = serializers.SerializerMethodField()
    # categories = CategorySerializer(many=True, read_only=True)
    stock_record = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='catalogue:product_detail',
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'structure',
            'image',
            'categories',
            'selling_price',
            'retail_price',
            'description',
            'product_rating',
            'product_rating_count',
            'detail_url',
            'attribute_summary',
            'image_list',
            'additional_information',
            'ingredients',
            'benefits',
            'stock_record',
            'url',
            'children',
        )

        read_only_fields = (
            'id',
            'image',
            'structure',
            'selling_price',
            'retail_price',
            'detail_url',
            'attribute_summary',
            'image_list',
            'stock_record',
            'children',
        )

    def get_image(self, obj):
        image = obj.primary_image()
        if hasattr(image, 'original'):
            return image.original.url
        return None

    def get_image_list(self, obj):
        image_list = obj.get_all_images()
        images_list = []
        for obj in image_list:
            image_dict = {
                'image': obj.original.url,
                'caption': obj.caption,
                'display_order': obj.display_order,
            }
            images_list.append(image_dict)
        return images_list

    def get_stock_record(self, obj):
        stock_record_list = []
        stock_list = obj.stockrecords.all()
        for obj in stock_list:
            stock_dict = {
                'partner_sku': obj.partner_sku,
                'num_in_stock': obj.num_in_stock,
                'num_allocated': obj.num_allocated,
                'low_stock_threshold': obj.low_stock_threshold,
            }
            stock_record_list.append(stock_dict)
        return stock_record_list
