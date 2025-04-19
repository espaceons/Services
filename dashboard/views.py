
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
@login_required # Seuls les utilisateurs connectés peuvent accéder à cette vue
def client_dashboard(request):
    # L'utilisateur connecté est accessible via request.user
    user = request.user

    # Récupérez ici les données spécifiques à cet utilisateur pour le tableau de bord
    # Par exemple :
    # user_orders = Order.objects.filter(user=user) # Si vous avez un modèle Order
    # user_settings = UserProfileSettings.objects.get_or_create(user=user)[0] # Si vous avez un modèle de paramètres
    # personalized_content = get_personalized_content(user) # Fonction pour obtenir du contenu personnalisé

    context = {
        'user': user,
        'page_title': 'Mon Tableau de Bord',
        # Ajoutez les données récupérées au contexte
        # 'orders': user_orders,
        # 'settings': user_settings,
        # 'personalized_items': personalized_content,
        'welcome_message': f"Bonjour, {user.username} ! Bienvenue sur votre tableau de bord."
    }
    return render(request, 'dashboard/client_dashboard.html', context)