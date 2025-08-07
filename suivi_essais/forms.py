from django import forms
from .models import Affaire, Essai, Carottage, Sondage, Permeabilite



class AffaireForm(forms.ModelForm):
    class Meta:
        model = Affaire
        fields = ['code_affaire', 'nom_chantier', 'adresse', 'numero_os', 'date_limite', 'client', 'localisation', 'commentaires', 'etat']

class EssaiForm(forms.ModelForm):
    class Meta:
        model = Essai
        #exclude = ['date_creation']
        fields = [
            'type_essai',
            'affaire',
            'conducteur',
            'identifiant',
            'libelle',
            'ville',
            'rue',
            'etat',
            'commentaire',
            'commentaire_saisie',
            'date_limite_realisation',
            'date_programmation',
            'date_realisation',
            'date_enlevement',
            'date_rendu',
            'date_etiquette',
            'date_formulaire',
            #'date_creation',
            'date_cloture',
            'date_leve',
            'campagne_code_chantier',
            'os_libelle',
            'os_no_engagement',
            'os_no',
            'coord_lon',
            'coord_lat',
            'cc48_x',
            'cc48_y',
            'cc48_z',
            'prevoir_enlev',
        ]


class CarottageForm(forms.ModelForm):
    class Meta:
        model = Carottage
        fields = ['profondeur', 'diametre', 'nature_enrobe', 'epaisseur', 'observations']

class SondageForm(forms.ModelForm):
    class Meta:
        model = Sondage
        fields = ['profondeur', 'methode', 'resistance_sol', 'humidite', 'observations']

class PermeabiliteForm(forms.ModelForm):
    class Meta:
        model = Permeabilite
        fields = ['profondeur', 'debit', 'duree_mesure', 'perm_k', 'observations']



