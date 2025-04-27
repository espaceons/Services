from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class utilistaeur permettant de se connecter avec un email et un mot de passe
# et de créer un utilisateur avec un email et un mot de passe
# et de créer un super utilisateur avec un email et un mot de passe
# et de créer un utilisateur avec un email, un mot de passe et un nom d'utilisateur
#-------------------------------------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
# class CustoUser
#-----------------
# - email : email de l'utilisateur (unique)
# - username : nom d'utilisateur (unique)
# - phone : numéro de téléphone (optionnel)
# - is_active : utilisateur actif (par défaut True)
# - is_staff : utilisateur staff (par défaut False)
# - profile_picture : photo de profil (optionnel)
# - objects : manager pour créer des utilisateurs et super utilisateurs
# - -------------------------------

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        verbose_name="Photo de profil"
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Utilisez email comme identifiant
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email