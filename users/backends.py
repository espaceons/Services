# users/backends.py

from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class PhoneBackend(ModelBackend):
    """
    Backend personnalisé pour permettre la connexion avec le numéro de téléphone + mot de passe.
    """

    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            # Cherche l'utilisateur avec le numéro de téléphone fourni
            user = CustomUser.objects.get(phone=phone)
            # Vérifie que le mot de passe est correct et que l'utilisateur est actif
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except CustomUser.DoesNotExist:
            # Aucun utilisateur trouvé avec ce numéro de téléphone
            return None
