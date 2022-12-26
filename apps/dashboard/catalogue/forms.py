from apps.catalogue.models import category,product
from oscar.apps.dashboard.catalogue import forms as base_forms
from treebeard.forms import movenodeform_factory
from oscar.apps.catalogue.models import ProductClass
from django import forms

CategoryForm = movenodeform_factory(
    category,
    fields=['name', 'description', 'image', 'is_active', 'is_featured',],
)

class ProductClassForm(forms.ModelForm):
    
    class Meta:
        model = ProductClass
        fields = ("name",)


class productform(base_forms.ProductForm):

    class Meta:

        model = product
        fields = (
            'title','upc','product_image','description','benifit1','benifit2','is_discountable','is_active','is_featured'
        )
