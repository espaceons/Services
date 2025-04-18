# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard' # Facultatif mais recommandé pour les namespaces d'URL

urlpatterns = [
    path('', views.admin_dashboard, name='index'), # URL pour la page d'accueil du tableau de bord
    path('client/', views.client_dashboard, name='client_dashboard'), # URL pour le tableau de bord client
    
]