from django.urls import path
from .views import edit_profile, liste_utilisateurs, register, profile, upload_profile_pic, user_login, user_logout

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/upload-pic/', upload_profile_pic, name='upload_profile_pic'),
    path('liste_utilisateurs/', liste_utilisateurs, name='liste_utilisateurs'),
    
]