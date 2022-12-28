from django.shortcuts import render
from django.views.generic import TemplateView
from apps.catalogue.models import product

# Create your views here.

class HomepageView(TemplateView):

    template_name = 'home.html'
    model = product
    

    # def get_queryset(self):
    #     queryset = self.model.objects.filter(is_active=True).exclude(structure='child')

    #     return queryset
    

    def get_context_data(self, **kwargs):

        context = super(HomepageView,self).get_context_data(**kwargs)
        context['featured_product'] = product.objects.filter(is_featured=True).filter(structure='parent')
        
        return context


class productdetail(TemplateView):

    template_name = 'product.html'

    

    def get_context_data(self, **kwargs):

        context = super(productdetail,self).get_context_data(**kwargs)
        context['product'] = product.objects.filter(is_featured=True).filter(structure='parent')
        
        return context


  
