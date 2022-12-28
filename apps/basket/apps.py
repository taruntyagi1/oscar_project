import oscar.apps.basket.apps as apps
from oscar.core.loading import get_class
from django.conf.urls import url


class BasketConfig(apps.BasketConfig):
    name = 'apps.basket'

    def ready(self):
        super(BasketConfig,self).ready()
    #     self.summary_view = get_class('basket.views', 'CustomBasketView')
        
       

    # def get_urls(self):
    #     urls = []
    #     urls += [
    #         url(r'^$', self.summary_view.as_view(), name='summary'),
           
           
    #     ]
    #     return self.post_process_urls(urls)

        
