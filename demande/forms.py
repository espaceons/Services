# demande/forms.py
from django import forms
from .models import Demande
from articles.models import Article # Importer Article si nécessaire pour les choix

class ClientDemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        # Le client choisit l'article et donne les détails
        # Le client ne choisit pas le statut, la date_demande, date_fixee ou validee_par
        fields = ['article', 'details_service']
        widgets = {
            'article': forms.Select(attrs={'class': 'form-select'}), # Utilise form-select pour Bootstrap
            'details_service': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), # Utilise form-control et définit les lignes
        }
        

class SuperuserDemandeValidationForm(forms.ModelForm):
     class Meta:
         model = Demande
         # L'administrateur peut changer le statut et fixer la date
         # Il ne modifie généralement pas le client, l'article ou les détails initiaux ici
         fields = ['statut', 'date_fixee']
         widgets = {
             'statut': forms.Select(attrs={'class': 'form-select'}),
             'date_fixee': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}), # Input type datetime-local pour un sélecteur intégré
         }