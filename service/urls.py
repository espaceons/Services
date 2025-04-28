"""
URL configuration for service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # Importez include pour inclure les URLs d'autres applications

from django.conf import settings # Importez settings
from django.conf.urls.static import static # Importez static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # Inclure les URLs de l'application users
    path('admindashboard/', include('dashboard.urls')), # Inclure les URLs de votre tableau de bord
    path('articles/', include('articles.urls')), # Inclure les URLs de votre application articles
    path('demandes/', include('demande.urls')), # Inclure les URLs de votre application demande
    path('factures/', include('billing.urls')), # Inclure les URLs de votre application factures
]

# Ajoutez ceci SEULEMENT en mode DÉVELOPPEMENT (DEBUG=True)
# Ceci permet au serveur de développement de Django de servir les fichiers
# uploadés par les utilisateurs (fichiers media).
# NE PAS utiliser en production !
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Note : Les fichiers statiques (STATIC_URL) sont généralement servis
# automatiquement par runserver en mode DEBUG sans ajout ici.
