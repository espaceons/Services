
from django.urls import path
from . import views

app_name = 'factures' # Namespace pour les URLs de cette application

urlpatterns = [
    # --- URLs Côté Client ---
    path('my/', views.list_my_invoices, name='my_invoices'), # /factures/my/
    path('<int:pk>/', views.view_invoice_client, name='view_invoice_client'), # /factures/1/ (pour le client)


    # --- URLs Côté Superutilisateur/Staff ---

    path('', views.list_invoices_admin, name='list_all_invoices'), # /factures/ (liste générale pour admin)
    path('<int:pk>/', views.view_invoice_admin, name='view_invoice_admin'), # /factures/1/ (détails pour admin)
]