from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_args):
        """create user and save their credentials"""
        if not email:
            raise ValueError("User must have a valid email address")
        user = self.model(email=self.normalize_email(email), **extra_args)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Saves the user provided data """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
