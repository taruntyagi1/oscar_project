from oscar.apps.dashboard.catalogue.views import CategoryListView,CategoryCreateView,CategoryUpdateView,ProductClassCreateView,ProductClassListView,ProductClassUpdateView,ProductListView,ProductCreateUpdateView
from apps.catalogue.models import category,product
from apps.dashboard.catalogue.forms import CategoryForm,ProductClassForm,productform

from apps.dashboard.catalogue.tables import CategoryTable,ProductTable


class categorylist(CategoryListView):

    table_class = CategoryTable

class categorycreate(CategoryCreateView):
    form_class = CategoryForm
    template_name = 'catalogue/category_form.html'

class categoryupdate(CategoryUpdateView):
    form_class = CategoryForm
    template_name = 'catalogue/category_form.html'

class productclasslist(ProductClassListView):

    template_name = 'catalogue/product_class_list.html'


class productclasscreate(ProductClassCreateView):
    form_class = ProductClassForm

class productclassupdate(ProductClassUpdateView):
    form_class = ProductClassForm


class productupdate(ProductCreateUpdateView):

    form_class = productform
    template_name = 'catalogue/product_update.html'


class productlist(ProductListView):

    table_class = ProductTable