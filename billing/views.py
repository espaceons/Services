
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test # Pour restreindre l'accès
from .models import Invoice, InvoiceItem # Importez vos modèles Invoice et InvoiceItem
from django.contrib import messages # Optionnel pour les messages
from django.core.exceptions import PermissionDenied # Pour gérer les erreurs de permission



# Fonction de test pour vérifier si l'utilisateur est un membre du staff ou un superuser
# Assurez-vous que cette fonction est définie ou importée si elle est ailleurs
def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser

# --- Vues Côté Client ---

@login_required
def list_my_invoices(request):
    # Récupère seulement les factures associées à l'utilisateur connecté
    my_invoices = Invoice.objects.filter(client=request.user).order_by('-issue_date')
    context = {
        'invoices': my_invoices,
        'page_title': 'Mes Factures'
    }
    return render(request, 'billing/my_invoices.html', context)

@login_required
def view_invoice_client(request, pk):
    # Récupère une facture spécifique
    invoice = get_object_or_404(Invoice, pk=pk)

    # === Vérification de la Propriété ===
    # S'assure que la facture appartient bien à l'utilisateur connecté
    if invoice.client != request.user:
        messages.error(request, "Vous n'avez pas la permission de voir cette facture.")
        raise PermissionDenied("Vous n'êtes pas le client de cette facture.")
    # ====================================

    # Récupère les éléments de la facture
    invoice_items = invoice.items.all() # Utilise le related_name='items' défini dans le modèle InvoiceItem

    context = {
        'invoice': invoice,
        'invoice_items': invoice_items,
        'page_title': f'Facture #{invoice.invoice_number}'
    }
    return render(request, 'billing/invoice_detail_client.html', context)


# --- Vues Côté Superutilisateur/Staff ---

# Ces vues sont accessibles uniquement aux utilisateurs ayant le statut de staff ou de superutilisateur.
# liste de tous les factures et détails d'une facture spécifique.
#-----------------------------------------------------------


@user_passes_test(is_staff_or_superuser)
def list_invoices_admin(request):
    # Récupère toutes les factures
    all_invoices = Invoice.objects.all().order_by('-issue_date')
    context = {
        'invoices': all_invoices,
        'page_title': 'Toutes les Factures'
    }
    return render(request, 'billing/all_invoices.html', context)

@user_passes_test(is_staff_or_superuser)
def view_invoice_admin(request, pk):
    # Récupère une facture spécifique (pas besoin de vérifier le client pour l'admin)
    invoice = get_object_or_404(Invoice, pk=pk)

    # Récupère les éléments de la facture
    invoice_items = invoice.items.all()

    context = {
        'invoice': invoice,
        'invoice_items': invoice_items,
        'page_title': f'Facture #{invoice.invoice_number} (Admin)'
    }
    return render(request, 'billing/invoice_detail_admin.html', context)