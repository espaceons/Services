from django.db import models
from django.conf import settings
from django.utils import timezone
from articles.models import Article # Importer le modèle Article

class Demande(models.Model):
    # Statuts possibles d'une demande
    STATUT_CHOICES = [
        ('en_attente', 'En attente de validation'),
        ('acceptee', 'Acceptée'),
        ('rejetee', 'Rejetée'),
        ('completee', 'Complétée'),
        ('annulee', 'Annulée'), # Un client pourrait annuler
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='demandes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='demandes_liees')
    details_service = models.TextField(help_text="Décrivez le service que vous demandez pour cet article.")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_demande = models.DateTimeField(auto_now_add=True)
    date_fixee = models.DateTimeField(null=True, blank=True, help_text="Date fixée par l'administrateur si la demande est acceptée.")
    validee_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='demandes_validees')
    # Vous pourriez ajouter un champ pour les commentaires de l'administrateur en cas de rejet par exemple

    def __str__(self):
        return f"Demande de {self.client.username} pour {self.article.title} - Statut: {self.statut}"

    class Meta:
        ordering = ['-date_demande'] # Trie les demandes par date de demande décroissante