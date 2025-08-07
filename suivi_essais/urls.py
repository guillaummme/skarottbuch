from django.urls import path
from . import views
from .views import import_essais_from_excel
from .views import liste_affaires , affaire_detail



app_name = 'suivi_essais'

urlpatterns = [
    #path('', views.affaire_list, name='affaire_list'),
    path('', views.liste_affaires, name='affaire_list'),
    path('affaire/<int:affaire_id>/', views.affaire_detail, name='affaire_detail'),
    #path('', affaire_list, name='affaire_list'),
    #path('affaire/<int:affaire_id>/', affaire_detail, name='affaire_detail'),
    #path('affaire/<int:affaire_id>/', views.affaire_detail, name='affaire_detail'),

    #path('affaire/<int:pk>/', views.affaire_detail, name='affaire_detail'),
    path('affaire/add/', views.affaire_create, name='affaire_create'),
    path('affaire/<int:pk>/add-essai/', views.essai_create, name='essai_create'),
    path('affaire/<int:pk>/upload-photo/', views.upload_photo, name='upload_photo'),
    path('essai/<int:pk>/', views.essai_detail, name='essai_detail'),
    path('essai/<int:pk>/edit/', views.essai_edit, name='essai_edit'),
    path('import_excel/', import_essais_from_excel, name='import_excel'),
    path('etiquettes/', views.liste_essais, name='liste_essais'),

]
