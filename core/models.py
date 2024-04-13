from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create my MyUserManager here.
class MyUserManager(BaseUserManager):
    def _create_user(self, username, email, password, refresh_token, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password must be provided")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        
        user.set_password()
        user.save()
        return user
    
    def create_user(self, username, email, password, refresh_token, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(self, username, email, password, refresh_token, **extra_fields)

    def create_superuser(self, username, email, password, refresh_token, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(self, username, email, password, refresh_token, **extra_fields)



# Create my User here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(max_length=254)
    refresh_token = models.CharField(max_length=254)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

