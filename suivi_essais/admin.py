from django.contrib import admin
from .models import (
    Client, Etat, Affaire, Essai, LogEtat,
    Carottage, Sondage, Permeabilite
)
from .models import PhotoAffaire
admin.site.register(PhotoAffaire)


class EssaiInline(admin.TabularInline):
    model = Essai
    extra = 1
    fields = ('libelle', 'type_essai', 'etat', 'date_realisation', 'conducteur')

@admin.register(Affaire)
class AffaireAdmin(admin.ModelAdmin):
    list_display = ('code_affaire', 'nom_chantier', 'client', 'etat', 'date_limite')
    search_fields = ('code_affaire', 'nom_chantier', 'client__nom')
    inlines = [EssaiInline]

@admin.register(Essai)
class EssaiAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'type_essai', 'affaire', 'etat', 'date_realisation')
    list_filter = ('type_essai', 'etat')
    search_fields = ('libelle', 'affaire__code_affaire')

admin.site.register(Carottage)
admin.site.register(Sondage)
admin.site.register(Permeabilite)
admin.site.register(Client)
admin.site.register(Etat)
admin.site.register(LogEtat)
