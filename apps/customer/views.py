from oscar.apps.customer.views import (
    AccountAuthView,)

from .forms import (
   
    CustomAuthenticationForm,
    
)



class LoginView(AccountAuthView):
    """
    A view for login
    """

    template_name = 'customer/profile/login.html'
    login_form_class = CustomAuthenticationForm