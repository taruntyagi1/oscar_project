from django.db import models
from oscar.apps.customer.abstract_models import AbstractUser,UserManager

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=300,unique=True)
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    login_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','username']


    def __str__(self):
        return self.username


    def has_perm(self,obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
