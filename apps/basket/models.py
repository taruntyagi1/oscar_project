from oscar.apps.basket.abstract_models import *



class Basket(AbstractBasket):
    def save(self,*args,**kwargs):
        self.reset_offer_applications()
        super(self.__class__,self).save(*args,**kwargs)






from oscar.apps.basket.models import *  # noqa isort:skip
