import oscar.apps.customer.apps as apps
from oscar.core.loading import get_class
from django.urls import path, re_path


class CustomerConfig(apps.CustomerConfig):
    name = 'apps.customer'


    def ready(self):
        from django.contrib.auth.forms import SetPasswordForm

        super(CustomerConfig, self).ready()
        self.login_view = get_class('customer.views', 'LoginView')

    