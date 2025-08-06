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


class Essai(models.Model):
    TYPE_ESSAI = [
        ('CAROTTE', 'Carottage'),
        ('SONDAGE', 'Sondage'),
        ('PERMEA', 'Perméabilité'),
    ]

    affaire = models.ForeignKey(Affaire, on_delete=models.CASCADE, related_name='essais')
    type_essai = models.CharField(max_length=20, choices=TYPE_ESSAI)
    nom = models.CharField(max_length=100, help_text="Ex: 2025_ACHENHEIM_CHARMES_C01", default="NOUVEL_ESSAI")
    date_realisation = models.DateField(null=True, blank=True)
    conducteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    etat = models.ForeignKey(Etat, on_delete=models.PROTECT)
    fichier_rapport = models.FileField(upload_to="rapports/", blank=True, null=True)

    def __str__(self):
        return f"{self.nom}"


class LogEtat(models.Model):
    essai = models.ForeignKey(Essai, on_delete=models.CASCADE)
    etat = models.ForeignKey(Etat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_log = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True)
from django.db import models

# Create your models here.
