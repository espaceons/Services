# articles/urls.py
from django.urls import path
from . import views

app_name = 'articles' # Namespace pour les URLs de cette application

urlpatterns = [
    path('', views.article_list, name='article_list'), # /articles/
    path('create/', views.article_create, name='article_create'), # /articles/create/
    path('<int:pk>/update/', views.article_update, name='article_update'), # /articles/1/update/
    path('<int:pk>/delete/', views.article_delete, name='article_delete'), # /articles/1/delete/
]