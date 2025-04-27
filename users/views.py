from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from users.models import CustomUser
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required, user_passes_test


# inscription nouveau utilisateur :
#----------------------------------
# - POST : créer un utilisateur et le connecter
# - GET : afficher le formulaire d'inscription
#----------------------------------

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})


# Login utilisateur :
#-------------------------
# - POST : authentifier l'utilisateur et le connecter
# - GET : afficher le formulaire de connexion
#-------------------------

# users/views.py
from django.shortcuts import render, redirect # Assurez-vous que 'redirect' est importé
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login # Assurez-vous que 'authenticate' et 'login' sont importés
from django.contrib import messages # Assurez-vous que 'messages' est importé si vous l'utilisez

# Assurez-vous que cette fonction est mappée à une URL dans votre urls.py
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password) # Passez request à authenticate si vous utilisez des backends d'authentification qui en ont besoin
            if user is not None:
                login(request, user) # Connecte l'utilisateur à la session

                # === LOGIQUE DE REDIRECTION CONDITIONNELLE ===
                # Vérifie si l'utilisateur est un membre du staff ou un superutilisateur
                if user.is_staff or user.is_superuser:
                    # Si oui, redirige vers la page du tableau de bord administrateur
                    # Assurez-vous que 'dashboard:index' correspond bien au nom de votre URL du tableau de bord
                    return redirect('dashboard:index')
                else:
                    # Sinon (utilisateur normal), redirige vers la page de profil
                    return redirect('dashboard:client_dashboard') # 'dashboard:client_dashboard' correspond bien au tableau de bord client
                # === FIN DE LA LOGIQUE DE REDIRECTION ===

            else:
                # Si authenticate a renvoyé None (identifiants invalides)
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
             # Si le formulaire n'est pas valide (erreurs de validation, e.g., champs vides)
             # Les erreurs du formulaire sont généralement affichées dans le template
             pass # Laissez le code passer pour afficher le formulaire avec les erreurs

    else:
        # Si la méthode est GET, afficher un formulaire vide
        form = AuthenticationForm()

    # Rendre le template de connexion avec le formulaire (vide pour GET, avec données/erreurs pour POST invalide)
    return render(request, 'users/login.html', {'form': form})

# Logout utilisateur :
#-------------------------
# - POST : déconnecter l'utilisateur
# - GET : rediriger vers la page de connexion
#-------------------------

@login_required
def user_logout(request):
    logout(request)
    return redirect('users:login')  # Redirige vers la page de connexion après déconnexion

# Profile utilisateur :
#-------------------------
# - GET : afficher le profil de l'utilisateur connecté
#-------------------------

@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def upload_profile_pic(request):
    if request.method == 'POST' and 'profile_picture' in request.FILES:
        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()
    return redirect('users:profile')


# liste des utilisateurs:

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def liste_utilisateurs(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'users/liste_utilisateurs.html', {'users': users})