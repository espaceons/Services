# articles/forms.py
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'published_date'] # Champs modifiables via le formulaire
        # ajouter des widgets pour styliser avec Bootstrap
        widgets = {
             'title': forms.TextInput(attrs={'class': 'form-control'}),
             'content': forms.Textarea(attrs={'class': 'form-control'}),
             'published_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}), # Exemple pour un date/heure picker
        }