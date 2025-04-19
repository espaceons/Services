# billing/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from demande.models import Demande # Importer le modèle Demande
import uuid # Pour générer des numéros de facture uniques

class Invoice(models.Model):
    # Statuts possibles d'une facture
    STATUT_CHOICES = [
        ('pending', 'En attente de paiement'),
        ('paid', 'Payée'),
        ('cancelled', 'Annulée'),
        ('due', 'Due'), # Facultatif : pour les factures en retard
        ('refunded', 'Remboursée'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    # Optionnel : Si une facture peut regrouper plusieurs demandes, gérez la relation ici ou via InvoiceItem
    # demande = models.ForeignKey(Demande, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')

    invoice_number = models.CharField(max_length=50, unique=True, default=uuid.uuid4) # Numéro de facture unique
    issue_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField() # Date d'échéance
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Montant total de la facture
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='pending')
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices_generated')
    paid_date = models.DateTimeField(null=True, blank=True) # Date de paiement si statut est 'paid'

    def __str__(self):
        return f"Facture #{self.invoice_number} pour {self.client.username}"

    def calculate_total_amount(self):
        # Méthode pour calculer le total en additionnant les totaux de chaque ligne
        total = sum(item.line_total for item in self.items.all())
        self.total_amount = total
        self.save() # Sauvegarde la facture avec le nouveau total

    class Meta:
        ordering = ['-issue_date']

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items') # Lien vers la facture parente
    # Lien vers la demande spécifique si cette ligne concerne une demande particulière
    demande = models.ForeignKey(Demande, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_items')

    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Montant total de cette ligne

    def save(self, *args, **kwargs):
        # Calcule le total de la ligne avant de sauvegarder
        self.line_total = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # Après sauvegarde, met à jour le total de la facture parente
        if self.invoice:
            self.invoice.calculate_total_amount()

    def __str__(self):
        return f"Ligne Facture pour {self.description} sur Facture #{self.invoice.invoice_number}"