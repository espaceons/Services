# demande/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test # Pour restreindre l'accès
from .models import Demande
from .forms import ClientDemandeForm, SuperuserDemandeValidationForm
from django.contrib import messages # Pour afficher des messages (optionnel)

from django.views.decorators.http import require_POST # Pour accepter seulement les requêtes POST
from django.core.exceptions import PermissionDenied # Pour gérer les erreurs de permission


# --- Vues Côté Client ---
# creation d'une nouvelle demande
# Assurez-vous que l'utilisateur est connecté avant de lui permettre de soumettre une demande
#--------------------------------------------------------------

@login_required
def create_demande(request):
    if request.method == 'POST':
        form = ClientDemandeForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.client = request.user # Assigne l'utilisateur connecté comme client
            demande.save()
            messages.success(request, "Votre demande a été soumise avec succès et en attente de validation.")
            return redirect('demande:my_demandes') # Redirige vers la liste des demandes du client
        else:
             messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ClientDemandeForm()
    context = {
        'form': form,
        'page_title': 'Soumettre une Nouvelle Demande'
    }
    return render(request, 'demande/demande_form_client.html', context) # Template pour le formulaire client


# Liste des demandes faites par l'utilisateur connecté
#--------------------------------------------------------------
# Assurez-vous que l'utilisateur est connecté avant de lui permettre de voir ses demandes
#--------------------------------------------------------------

@login_required
def list_my_demandes(request):
    """
    Affiche les demandes de l'utilisateur connecté, avec filtrage optionnel par statut
    """
    # Initialise le queryset de base avec toutes les demandes de l'utilisateur
    demandes = Demande.objects.filter(client=request.user)
    
    # Applique le filtre si un statut est spécifié
    statut = request.GET.get('statut')
    if statut:
        demandes = demandes.filter(statut=statut)
    
    context = {
        'demandes': demandes,
        'page_title': 'Mes Demandes',
        'total_demandes': demandes.count(),
    }
    return render(request, 'demande/my_demandes.html', context)



# Détails d'une demande spécifique faite
# par l'utilisateur connecté
# Assurez-vous que l'utilisateur est connecté avant de lui permettre de voir les détails de sa demande
# Utilise get_object_or_404 pour gérer le cas où la demande n'existe pas ou n'appartient pas à l'utilisateur
#--------------------------------------------------------------


@login_required
def view_my_demande(request, pk):
    # Récupère une demande spécifique faite par l'utilisateur connecté
    # Utilise get_object_or_404 pour gérer le cas où la demande n'existe pas ou n'appartient pas à l'utilisateur
    demande = get_object_or_404(Demande, pk=pk, client=request.user)
    context = {
        'demande': demande,
        'page_title': f'Détail de la Demande #{demande.pk}'
    }
    return render(request, 'demande/demande_detail_client.html', context) # Template pour les détails côté client


# --- Vues Côté Superutilisateur/Staff ---

# Fonction de test (si elle n'est pas déjà importée ou définie)
# Assurez-vous que l'utilisateur est soit un superutilisateur, soit un membre du personnel
#--------------------------------------------------------------


def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser


# Liste de toutes les demandes (pour le personnel ou superutilisateur)
# Assurez-vous que l'utilisateur est soit un superutilisateur, soit un membre du personnel
#--------------------------------------------------------------


@user_passes_test(is_staff_or_superuser)
def list_all_demandes(request):

    statut = request.GET.get('statut')  # Récupère le paramètre ?statut=xxx

    # Récupère toutes les demandes (ou seulement celles en attente si vous préférez)
    all_demandes = Demande.objects.all()
    if statut:
        all_demandes = all_demandes.filter(statut=statut) # application du filtre

    # all_demandes = Demande.objects.filter(statut='en_attente') # Exemple pour afficher seulement les demandes en attente
    context = {
        'demandes': all_demandes,
        'page_title': 'Toutes les Demandes'
    }
    return render(request, 'demande/all_demandes.html', context) # Template pour lister toutes les demandes


# Détails d'une demande spécifique (pour le personnel ou superutilisateur)
# Assurez-vous que l'utilisateur est soit un superutilisateur, soit un membre du personnel
#--------------------------------------------------------------


@user_passes_test(is_staff_or_superuser)
def validate_demande(request, pk):
    demande = get_object_or_404(Demande, pk=pk)
    if request.method == 'POST':
        form = SuperuserDemandeValidationForm(request.POST, instance=demande)
        if form.is_valid():
            # Assigne l'administrateur connecté comme valideur si le statut change et que le champ est nul
            if demande.statut != form.cleaned_data['statut'] and demande.validee_par is None:
                 demande.validee_par = request.user
            form.save()
            messages.success(request, f"La demande #{demande.pk} a été mise à jour.")
            return redirect('demande:list_all_demandes') # Redirige vers la liste de toutes les demandes
        else:
             messages.error(request, "Veuillez corriger les erreurs de validation.")
    else:
        form = SuperuserDemandeValidationForm(instance=demande)
    context = {
        'form': form,
        'demande': demande,
        'page_title': f'Valider Demande #{demande.pk}'
    }
    return render(request, 'demande/demande_validation_form.html', context) # Template pour le formulaire de validation


# Détails d'une demande spécifique (pour le personnel ou superutilisateur)
# Assurez-vous que l'utilisateur est soit un superutilisateur, soit un membre du personnel
#--------------------------------------------------------------


@user_passes_test(is_staff_or_superuser)
def view_demande_admin(request, pk):
    # Vue pour afficher les détails d'une demande pour l'administrateur
    demande = get_object_or_404(Demande, pk=pk)
    context = {
        'demande': demande,
        'page_title': f'Détail Demande #{demande.pk} (Admin)'
    }
    return render(request, 'demande/demande_detail_admin.html', context) # Template pour les détails côté admin



# Vue pour accepter une demande (accessible seulement par superuser/staff et accepte seulement POST)
#---------------------------------------------------------------

@require_POST # S'assure que seule une requête POST est acceptée, sinon renvoie 405 Method Not Allowed
@user_passes_test(is_staff_or_superuser) # S'assure que seul un superuser/staff y a accès
def accept_demande(request, pk): # Prend l'ID de la demande depuis l'URL
    demande = get_object_or_404(Demande, pk=pk) # Récupère la demande

    # Vérification supplémentaire : s'assurer que la demande est bien en attente avant d'accepter
    if demande.statut == 'en_attente':
        demande.statut = 'acceptee' # Change le statut à 'acceptée'
        demande.validee_par = request.user # Assigne l'utilisateur connecté comme validateur
        # Note : La date_fixee n'est pas définie ici. Si vous voulez la définir lors de l'acceptation,
        # vous pourriez l'initialiser à timezone.now() ou nécessiter une autre étape/input.
        demande.save() # Enregistre les changements

        messages.success(request, f"La demande #{demande.pk} a été acceptée.")
    else:
         # Si la demande n'était pas en attente (déjà acceptée, rejetée, etc.)
         messages.warning(request, f"La demande #{demande.pk} ne peut pas être acceptée (statut actuel : {demande.get_statut_display}).")


    # Redirige généralement vers la page de détails de la demande pour voir le changement
    return redirect('demande:view_demande_admin', pk=demande.pk)

# Vous pourriez créer une vue similaire 'reject_demande' si nécessaire.


# === Vues Côté Client ===

# Modification d'une demande existante (pour le client)
# Assurez-vous que l'utilisateur est connecté avant de lui permettre de modifier sa demande
#--------------------------------------------------------------


@login_required
def update_demande_client(request, pk):
    demande = get_object_or_404(Demande, pk=pk)

    # === Vérifications : Propriétaire et Statut ===
    # Vérifie si l'utilisateur connecté est le propriétaire de la demande
    if demande.client != request.user:
        messages.error(request, "Vous n'avez pas la permission de modifier cette demande.")
        # Vous pourriez rediriger ou lever une erreur 403 Forbidden
        raise PermissionDenied("Vous n'êtes pas le propriétaire de cette demande.")

    # Vérifie si la demande est en attente
    if demande.statut != 'en_attente':
        messages.warning(request, f"Cette demande ne peut plus être modifiée (statut actuel : {demande.get_statut_display}).")
        # Redirige vers la page de détails de la demande
        return redirect('demande:view_my_demande', pk=demande.pk)
    # ==============================================

    if request.method == 'POST':
        form = ClientDemandeForm(request.POST, instance=demande) # Lie le formulaire aux données POST et à l'instance existante
        if form.is_valid():
            form.save()
            messages.success(request, "Votre demande a été modifiée avec succès.")
            return redirect('demande:view_my_demande', pk=demande.pk) # Redirige vers les détails après modification
        else:
             messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ClientDemandeForm(instance=demande) # Pré-remplit le formulaire avec les données actuelles
    context = {
        'form': form,
        'demande': demande, # Passe l'objet demande au template pour afficher des infos si besoin
        'page_title': f'Modifier Demande #{demande.pk}'
    }
    # Réutilise le template du formulaire client
    return render(request, 'demande/demande_form_client.html', context)

# Supprimer une demande existante (pour le client)
# Assurez-vous que l'utilisateur est connecté avant de lui permettre de supprimer sa demande
#--------------------------------------------------------------


@login_required
def delete_demande_client(request, pk):
    demande = get_object_or_404(Demande, pk=pk)

    # === Vérifications : Propriétaire et Statut ===
    # Vérifie si l'utilisateur connecté est le propriétaire de la demande
    if demande.client != request.user:
         messages.error(request, "Vous n'avez pas la permission de supprimer cette demande.")
         raise PermissionDenied("Vous n'êtes pas le propriétaire de cette demande.")

    # Vérifie si la demande est en attente
    if demande.statut != 'en_attente':
         messages.warning(request, f"Cette demande ne peut plus être supprimée (statut actuel : {demande.get_statut_display}).")
         return redirect('demande:view_my_demande', pk=demande.pk)
    # ==============================================

    if request.method == 'POST':
        demande.delete() # Supprime l'objet de la base de données
        messages.success(request, f"La demande #{demande.pk} a été supprimée avec succès.")
        return redirect('demande:my_demandes') # Redirige vers la liste des demandes après suppression

    # Afficher une page de confirmation avant de supprimer (méthode GET)
    context = {
        'demande': demande,
        'page_title': f'Confirmer Suppression Demande #{demande.pk}'
    }
    return render(request, 'demande/demande_confirm_delete_client.html', context)


# --- Vues Côté Superutilisateur/Staff ---
# ... (vos autres vues superuser comme list_all_demandes, view_demande_admin, accept_demande) ...