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
    @property
    def round_rating(self):
        if self.product_rating:
            return round(self.product_rating)
        return 0

    @property
    def variants_list(self):
        product_list = []
        if self.is_parent:
            for prod in self.children.public().order_by('stockrecords'):
                if hasattr(prod, 'stockrecords') and prod.stockrecords.first() and prod.stockrecords.first().num_in_stock > 0:
                    product_list.append(prod)
        return product_list

   

    @property
    def get_complete_title(self):
        if self.structure == "child":
            name = f"{self.parent.title} {self.title}"
        else:
            name = self.title
        return name

    @property
    def get_tag_line(self):
        if self.structure == "child":
            name = self.parent.tagline
        else:
            name = self.tagline
        return name
from oscar.apps.catalogue.models import *  # noqa isort:skip
