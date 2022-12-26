from oscar.apps.catalogue.abstract_models import *

class category(AbstractCategory):
    image = models.ImageField(upload_to='photo/category',null = True,blank = True)
    is_active = models.BooleanField(default=False,null=True,blank=True)
    is_featured = models.BooleanField(default=False,null=True,blank=True)


class product(AbstractProduct):
    product_image = models.ImageField(upload_to='photo/product',null = True,blank = True)
    benifit1 = models.CharField(max_length=300,null = True,blank = True)
    benifit2 = models.CharField(max_length=300,null = True,blank = True)
    is_active = models.BooleanField(default=False,null =True,blank=True)
    is_featured = models.BooleanField(default=False,null =True,blank =True)
from oscar.apps.catalogue.models import *  # noqa isort:skip
