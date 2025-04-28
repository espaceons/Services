
# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser
from .forms import ClientRegistrationForm, CustomUserCreationForm, ProfileUpdateForm, PhoneLoginForm

# Inscription d'un nouvel utilisateur
def register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Redirige vers la page de connexion après l'inscription
            return redirect('users:client_login')  # Redirection vers la vue de connexion
    else:
        form = ClientRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# Connexion pour les administrateurs (email + mot de passe)
def admin_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Vérifie si l'utilisateur est bien un admin ou un staff
            if user.is_superuser or user.is_staff:
                return redirect('dashboard:index')
            else:
                messages.error(request, "Accès réservé aux administrateurs.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/admin_login.html', {'form': form})

# Connexion pour les clients (téléphone + mot de passe)
def client_login_view(request):
    if request.method == 'POST':
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = authenticate(request, phone=phone, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard:client_dashboard')
            else:
                messages.error(request, "Numéro de téléphone ou mot de passe invalide.")
    else:
        form = PhoneLoginForm()

    return render(request, 'users/client_login.html', {'form': form})

# Déconnexion de l'utilisateur
@login_required
def user_logout(request):
    logout(request)
    return redirect('users:client_login')  # Redirection après déconnexion

# Affichage du profil utilisateur
@login_required
def profile(request):
    return render(request, 'users/profile.html')

# Modification du profil utilisateur
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

# Upload / Modification de la photo de profil
@login_required
def upload_profile_pic(request):
    if request.method == 'POST' and 'profile_picture' in request.FILES:
        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()
    return redirect('users:profile')

# Liste de tous les utilisateurs (réservée aux administrateurs)
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def liste_utilisateurs(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'users/liste_utilisateurs.html', {'users': users})
