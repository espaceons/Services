
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test # Pour restreindre l'accès
from django.contrib.auth import get_user_model # Pour accéder à votre modèle utilisateur
from django.contrib.auth.decorators import login_required

from articles.models import Article
from demande.models import Demande # Pour restreindre l'accès aux utilisateurs connectés
# Récupérez votre modèle utilisateur personnalisé
CustomUser = get_user_model()

# Fonction de test pour vérifier si l'utilisateur est un membre du staff ou un superuser
def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser


# Vue pour le tableau de bord administrateur
#------------------------------------------------


# Applique le décorateur pour restreindre l'accès à la vue
@user_passes_test(is_staff_or_superuser)
def admin_dashboard(request):
    # Récupérer les données à afficher sur le tableau de bord
    total_users = CustomUser.objects.count()
    total_articles = Article.objects.count()
    total_demandes = Demande.objects.count() # Nombre total de toutes les demandes

    # Ajoutez ici d'autres requêtes à la base de données pour obtenir des statistiques ou informations clés

    # === Compter les demandes par statut ===
    demandes_en_attente_count = Demande.objects.filter(statut='en_attente').count()
    demandes_acceptees_count = Demande.objects.filter(statut='acceptee').count()
    demandes_rejetee_count = Demande.objects.filter(statut='rejetee').count()
    demandes_completee_count = Demande.objects.filter(statut='completee').count()
    demandes_annulee_count = Demande.objects.filter(statut='annulee').count()
    # ======================================

    # Dernières demandes
    dernieres_demandes = Demande.objects.all().order_by('-date_demande')[:5]


    context = {
        'total_users': total_users,
        'total_articles': total_articles,
        'page_title': 'Tableau de Bord Administrateur', # Titre pour le template
        'total_demandes': total_demandes,

        # === les comptes par statut au contexte ===
        'demandes_en_attente_count': demandes_en_attente_count,
        'demandes_acceptees_count': demandes_acceptees_count,
        'demandes_rejetee_count': demandes_rejetee_count,
        'demandes_completee_count': demandes_completee_count,
        'demandes_annulee_count': demandes_annulee_count,
        # ================================================


        # Ajoutez d'autres données au contexte
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

# Note : vous pouvez aussi utiliser les classes de vues génériques de Django avec les Mixins
# comme LoginRequiredMixin et UserPassesTestMixin pour un contrôle d'accès basé sur les classes.


# Vue pour le tableau de bord client
@login_required
def client_dashboard(request):
    # Statistique des demande du client

    mes_demandes = Demande.objects.filter(client=request.user)
    context = {
        'page_title': 'Mon Tableau de Bord',
        'total_mes_demandes': mes_demandes.count(),
        'mes_demandes_en_attente': mes_demandes.filter(statut='en_attente').count(),
        'mes_demandes_acceptees': mes_demandes.filter(statut='acceptee').count(),
        'mes_demandes_rejetees': mes_demandes.filter(statut='rejetee').count(),
        'mes_demandes_completees': mes_demandes.filter(statut='completee').count(),
        'mes_demandes_annulees': mes_demandes.filter(statut='annulee').count(),
        'dernieres_demandes': mes_demandes.order_by('-date_demande')[:5]
    }
    return render(request, 'dashboard/client_dashboard.html', context)