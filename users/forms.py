# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser



# Inscription utilisateur :
#-------------------------
# - POST : créer un utilisateur et le connecter
# - GET : afficher le formulaire d'inscription
#-------------------------

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Champ email obligatoire
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = CustomUser
        fields = ("email","phone", "username", "password1", "password2")  # Retirez 'phone' s'il n'existe pas

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]  # Assure que l'email est bien enregistré
        if commit:
            user.save()
        return user
    
# ProfileUpdateForm:
#-------------------------
# - POST : mettre à jour le profil de l'utilisateur
# - GET : afficher le formulaire de mise à jour du profil
#-------------------------

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }



# Formulaire d'inscription d'un nouvel utilisateur par email
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Email obligatoire
    phone = forms.CharField(max_length=20, required=False)  # Téléphone optionnel

    class Meta:
        model = CustomUser
        fields = ("email", "phone", "username", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# Formulaire de connexion client par téléphone
class PhoneLoginForm(forms.Form):
    phone = forms.CharField(label="Téléphone", max_length=20)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class ClientRegistrationForm(UserCreationForm):
    phone = forms.CharField(label="Téléphone", max_length=20)
    username = forms.CharField(label="non d'utilisateur")

    class Meta:
        model = CustomUser
        fields = ("phone", "username", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data['phone']  # Attribuer le téléphone
        
        # Attribution d'un email temporaire
        user.email = f"{user.phone}@example.com"  # Email temporaire basé sur le téléphone

        if commit:
            user.save()  # Sauvegarder l'utilisateur
        return user

