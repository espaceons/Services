# users/urls.py

from django.urls import path
from .views import (
    register, profile, edit_profile, upload_profile_pic, 
    user_logout, admin_login_view, client_login_view, liste_utilisateurs
)

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),                   # Inscription
    path('admin-login/', admin_login_view, name='admin_login'),      # Connexion Admin
    path('', client_login_view, name='client_login'),   # Connexion Client
    path('logout/', user_logout, name='logout'),                     # Déconnexion
    path('profile/', profile, name='profile'),                       # Affichage du profil
    path('profile/edit/', edit_profile, name='edit_profile'),        # Modifier profil
    path('profile/upload-pic/', upload_profile_pic, name='upload_profile_pic'), # Upload photo de profil
    path('liste_utilisateurs/', liste_utilisateurs, name='liste_utilisateurs'), # Liste des utilisateurs
]
