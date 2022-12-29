from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,username,password=None):
        if not email:
            raise ValueError("Email is required")

        if not username:
            raise ValueError("username is required")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user


    def create_superuser(self,first_name,last_name,email,username,password = None):
        user = self.create_user(
            email = self.no(email),
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using = self._db)
        return user