# articles/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test # Pour restreindre l'accès
from .models import Article # Importez votre modèle Article
from .forms import ArticleForm # Vous devrez créer ce formulaire plus tard

# Fonction de test pour vérifier si l'utilisateur est un membre du staff ou un superuser
# Vous pouvez la définir ici ou l'importer si elle est définie ailleurs (par exemple dans votre app users ou dashboard)
def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser

# Vue pour lister les articles (accessible seulement par staff/superuser)
@user_passes_test(is_staff_or_superuser)
def article_list(request):
    articles = Article.objects.all() # Récupère tous les articles
    context = {
        'articles': articles,
        'page_title': 'Liste des Articles'
    }
    return render(request, 'articles/article_list.html', context)

# Vue pour créer un nouvel article (accessible seulement par staff/superuser)
@user_passes_test(is_staff_or_superuser)
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False) # Ne pas enregistrer tout de suite
            article.author = request.user # Assigne l'utilisateur connecté comme auteur
            article.save() # Enregistre l'article en base de données
            return redirect('articles:article_list') # Redirige après succès (assurez-vous du nom d'URL)
    else:
        form = ArticleForm()
    context = {
        'form': form,
        'page_title': 'Créer un Article'
    }
    return render(request, 'articles/article_form.html', context) # Réutilise potentiellement un template de formulaire


# Vue pour modifier un article existant (accessible seulement par staff/superuser)
@user_passes_test(is_staff_or_superuser)
def article_update(request, pk): # Capture la clé primaire de l'article depuis l'URL
    article = get_object_or_404(Article, pk=pk) # Récupère l'article ou renvoie 404
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article) # Lie le formulaire à l'instance existante
        if form.is_valid():
            form.save()
            return redirect('articles:article_list') # Redirige après succès
    else:
        form = ArticleForm(instance=article) # Pré-remplit le formulaire avec les données de l'article
    context = {
        'form': form,
        'article': article,
        'page_title': f'Modifier l\'Article: {article.title}'
    }
    return render(request, 'articles/article_form.html', context) # Réutilise potentiellement un template de formulaire

# Vue pour supprimer un article (accessible seulement par staff/superuser)
@user_passes_test(is_staff_or_superuser)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles:article_list') # Redirige après suppression
    context = {
        'article': article,
        'page_title': f'Supprimer l\'Article: {article.title}'
    }
    # Un template de confirmation est généralement utilisé
    return render(request, 'articles/article_confirm_delete.html', context)