# articles/models.py
from django.db import models
from django.conf import settings # importez settings pour accéder à AUTH_USER_MODEL
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # === C'est la bonne pratique pour référencer votre modèle utilisateur personnalisé ===
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    # ==================================================================================
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date'] # Trie les articles par date de publication décroissante