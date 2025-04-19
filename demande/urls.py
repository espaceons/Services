# demande/urls.py
from django.urls import path
from . import views

app_name = 'demande' # Namespace pour les URLs de cette application

urlpatterns = [
    # --- URLs Côté Client ---
    path('new/', views.create_demande, name='create_demande'), # /demandes/new/
    path('my/', views.list_my_demandes, name='my_demandes'), # /demandes/my/
    path('<int:pk>/', views.view_my_demande, name='view_my_demande'), # /demandes/1/ (pour le client)
    
    # === URLs pour modification et suppression demande client ===
    path('<int:pk>/update/', views.update_demande_client, name='update_demande_client'), # /demandes/1/update/
    path('<int:pk>/delete/', views.delete_demande_client, name='delete_demande_client'), # /demandes/1/delete/ (pour confirmation GET et suppression POST)
    # ===========================================================


    # --- URLs Côté Superutilisateur/Staff ---
    path('', views.list_all_demandes, name='list_all_demandes'), # /demandes/ (liste générale pour admin)
    path('<int:pk>/validate/', views.validate_demande, name='validate_demande'), # /demandes/1/validate/
    path('<int:pk>/admin/', views.view_demande_admin, name='view_demande_admin'), # /demandes/1/admin/ (détails pour admin)

    # === URL pour accepter une demande ===
    path('<int:pk>/accept/', views.accept_demande, name='accept_demande'), # /demandes/1/accept/
]