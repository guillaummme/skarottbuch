from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    nom = models.CharField(max_length=255)
    contact = models.CharField(max_length=255, blank=True)
    adresse = models.TextField(blank=True)

    def __str__(self):
        return self.nom

class Etat(models.Model):
    code = models.IntegerField(primary_key=True)
    libelle = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.libelle}"

class Affaire(models.Model):
    code_affaire = models.CharField(max_length=50, unique=True, help_text="Ex: 2542/001")
    nom_chantier = models.CharField(max_length=255, help_text="Nom ou lieu du chantier")
    adresse = models.CharField(max_length=255, blank=True)
    numero_os = models.CharField("Numéro d'ordre de service", max_length=100, blank=True)
    date_limite = models.DateField(null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    localisation = models.CharField(max_length=255, blank=True)
    commentaires = models.TextField(blank=True)
    etat = models.ForeignKey(Etat, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.code_affaire} | {self.nom_chantier}"


from django.db import models

class Essai(models.Model):
    TYPE_CHOICES = [
        ('CAROTTE', 'Carottage'),
        ('SONDAGE', 'Sondage'),
        ('PERMEA', 'Perméabilité'),
    ]
    identifiant = models.CharField(max_length=50, blank=False, null=False, unique=True)

    type_essai = models.CharField(max_length=20, choices=TYPE_CHOICES)
    affaire = models.ForeignKey("Affaire", on_delete=models.CASCADE, related_name="essais")

    conducteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    #identifiant = models.CharField(max_length=50, blank=True, null=True)
    libelle = models.CharField(max_length=255)  # ex: 2025_ACHENHEIM_CHARMES_C01
    ville = models.CharField(max_length=100, blank=True, null=True)
    rue = models.CharField(max_length=255, blank=True, null=True)

    etat = models.ForeignKey("Etat", on_delete=models.SET_NULL, null=True)
    commentaire = models.TextField(blank=True, null=True)
    commentaire_saisie = models.TextField(blank=True, null=True)

    date_limite_realisation = models.DateField(blank=True, null=True)
    date_programmation = models.DateField(blank=True, null=True)
    date_realisation = models.DateField(blank=True, null=True)
    date_enlevement = models.DateField(blank=True, null=True)
    date_rendu = models.DateField(blank=True, null=True)

    date_etiquette = models.DateField(blank=True, null=True)
    date_formulaire = models.DateField(blank=True, null=True)
    #date_creation = models.DateField(blank=True, null=True)
    date_creation = models.DateField(auto_now_add=True)
    date_cloture = models.DateField(blank=True, null=True)
    date_leve = models.DateField(blank=True, null=True)

    campagne_code_chantier = models.CharField(max_length=50, blank=True, null=True)

    os_libelle = models.CharField(max_length=255, blank=True, null=True)
    os_no_engagement = models.CharField(max_length=50, blank=True, null=True)
    os_no = models.CharField(max_length=50, blank=True, null=True)

    coord_lon = models.FloatField(blank=True, null=True)
    coord_lat = models.FloatField(blank=True, null=True)

    cc48_x = models.FloatField(blank=True, null=True)
    cc48_y = models.FloatField(blank=True, null=True)
    cc48_z = models.FloatField(blank=True, null=True)

    prevoir_enlev = models.BooleanField(default=False)

    def __str__(self):
        return self.libelle or f"{self.type} sans nom"



class LogEtat(models.Model):
    essai = models.ForeignKey(Essai, on_delete=models.CASCADE)
    etat = models.ForeignKey(Etat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_log = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True)
from django.db import models

class Carottage(models.Model):
    essai = models.OneToOneField('Essai', on_delete=models.CASCADE)
    profondeur = models.DecimalField(max_digits=5, decimal_places=1, help_text="Profondeur en cm")
    diametre = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="Diamètre en cm")
    nature_enrobe = models.CharField(max_length=100, blank=True)
    epaisseur = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text="Épaisseur en cm")
    observations = models.TextField(blank=True)

class Sondage(models.Model):
    essai = models.OneToOneField('Essai', on_delete=models.CASCADE)
    profondeur = models.DecimalField(max_digits=5, decimal_places=2)
    methode = models.CharField(max_length=100, blank=True)
    resistance_sol = models.CharField(max_length=100, blank=True)
    humidite = models.CharField(max_length=100, blank=True)
    observations = models.TextField(blank=True)

class Permeabilite(models.Model):
    essai = models.OneToOneField('Essai', on_delete=models.CASCADE)
    profondeur = models.DecimalField(max_digits=5, decimal_places=2)
    debit = models.DecimalField(max_digits=6, decimal_places=2)
    duree_mesure = models.IntegerField(help_text="Durée en secondes", null=True, blank=True)
    perm_k = models.DecimalField("Coefficient k (m/s)", max_digits=8, decimal_places=6, null=True, blank=True)
    observations = models.TextField(blank=True)

class PhotoAffaire(models.Model):
    affaire = models.ForeignKey('Affaire', on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos_affaires/')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo pour {self.affaire.code_affaire}"

# Create your models here.
