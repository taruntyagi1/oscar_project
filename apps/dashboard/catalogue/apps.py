import oscar.apps.dashboard.catalogue.apps as apps



class CatalogueDashboardConfig(apps.CatalogueDashboardConfig):
    name = 'apps.dashboard.catalogue'

    def ready(self):
        super(CatalogueDashboardConfig,self).ready()

        from .views import (
            categoryupdate,categorycreate,categorylist,productclasslist,productclasscreate,productclassupdate,productlist,productupdate
        )

        self.category_create_view = categorycreate
        self.category_update_view = categoryupdate
        self.category_list_view = categorylist
        self.product_class_list_view = productclasslist
        self.product_class_create_view = productclasscreate
        self.product_class_update_view = productclassupdate
        self.product_list_view = productlist
        self.product_createupdate_view = productupdate




