from django.shortcuts import render
from django.views.generic import TemplateView
from apps.catalogue.models import product

# Create your views here.

class HomepageView(TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):

        context = super(HomepageView,self).get_context_data(**kwargs)
        context['get_product'] = product.objects.filter(is_featured=True)
        
        return context
