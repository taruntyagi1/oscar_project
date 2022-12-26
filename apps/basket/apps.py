import oscar.apps.basket.apps as apps


class BasketConfig(apps.BasketConfig):
    name = 'apps.basket'

    def ready(self):
        super(BasketConfig,self).ready()

        
