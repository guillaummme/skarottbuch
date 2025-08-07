from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Affaire, Etat, Essai, Carottage, Sondage, Permeabilite, PhotoAffaire
from .import_excel import importer_essais_depuis_excel
from .pdf.etiquettes import generate_etiquette_pdfs_for_essais
from django.http import FileResponse

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404


from .forms import (
    AffaireForm, EssaiForm, CarottageForm,
    SondageForm, PermeabiliteForm
)

def liste_affaires(request):
    etat = request.GET.get("etat")
    print(f"[DEBUG] etat sélectionné : {etat}")

    adresse = request.GET.get("adresse")
    recherche = request.GET.get("q")

    affaires = Affaire.objects.annotate(nb_essais=Count("essais"))

    if etat:
        try:
            affaires = affaires.filter(etat__code=int(etat))
        except ValueError:
            pass  # Ignore si "etat" n'est pas un entier valide

    if adresse:
        affaires = affaires.filter(adresse__icontains=adresse)

    if recherche:
        affaires = affaires.filter(
            Q(nom_chantier__icontains=recherche) |
            Q(adresse__icontains=recherche) |
            Q(essais__identifiant__icontains=recherche)
        ).distinct()

    # ✅ Charger tous les états disponibles
    etats = Etat.objects.all()

    context = {
        "affaires": affaires,
        "etats": etats,
        "etat_selectionne": etat,
        "adresse_recherchee": adresse,
        "recherche": recherche,
    }

    return render(request, "suivi_essais/liste_affaires.html", context)

def liste_essais(request):
    essais = Essai.objects.select_related("affaire").all().order_by("-date_creation")

    date_debut = request.POST.get('date_debut')
    date_fin = request.POST.get('date_fin')
    code_affaire = request.POST.get('code_affaire')

    if date_debut:
        essais = essais.filter(date_creation__gte=parse_date(date_debut))
    if date_fin:
        essais = essais.filter(date_creation__lte=parse_date(date_fin))
    if code_affaire:
        essais = essais.filter(affaire__code_affaire__icontains=code_affaire)

    if request.method == "POST" and "generer_pdf" in request.POST:
        selected_ids = request.POST.getlist('essais')
        essais_selectionnes = essais.filter(id__in=selected_ids)
        pdf_path = generate_etiquette_pdfs_for_essais(essais_selectionnes)
        return FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename="etiquettes.pdf")

    return render(request, 'suivi_essais/liste_essais.html', {
        'essais': essais,
        'date_debut': date_debut,
        'date_fin': date_fin,
        'code_affaire': code_affaire,
    })


def affaire_detail(request, affaire_id):
    affaire = get_object_or_404(Affaire, id=affaire_id)
    essais = affaire.essais.all()
    return render(request, "suivi_essais/affaire_detail.html", {
        "affaire": affaire,
        "essais": essais,
    })

def affaire_create(request):
    if request.method == 'POST':
        form = AffaireForm(request.POST)
        if form.is_valid():
            affaire = form.save()
            return redirect('suivi_essais:affaire_detail', pk=affaire.pk)
    else:
        form = AffaireForm()
    return render(request, 'suivi_essais/affaire_form.html', {'form': form})


def essai_create(request, pk):
    affaire = get_object_or_404(Affaire, pk=pk)
    if request.method == 'POST':
        form = EssaiForm(request.POST)
        if form.is_valid():
            essai = form.save(commit=False)
            essai.affaire = affaire
            essai.save()

            # Créer l'entrée correspondante selon le type d'essai
            if essai.type_essai == 'CAROTTE':
                Carottage.objects.create(essai=essai, profondeur=0)

            elif essai.type_essai == 'SONDAGE':
                Sondage.objects.create(essai=essai, profondeur=0)
            elif essai.type_essai == 'PERMEA':
                Permeabilite.objects.create(essai=essai, profondeur=0, debit=0)

            return redirect('suivi_essais:affaire_detail', pk=pk)
    else:
        form = EssaiForm()
    return render(request, 'suivi_essais/essai_form.html', {'form': form, 'affaire': affaire})


from django.shortcuts import render




from django.shortcuts import render, get_object_or_404, redirect
from .models import Affaire, PhotoAffaire

def upload_photo(request, pk):
    affaire = get_object_or_404(Affaire, pk=pk)
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        for f in files:
            PhotoAffaire.objects.create(affaire=affaire, image=f)
        return redirect('suivi_essais:affaire_detail', pk=pk)
    return render(request, 'suivi_essais/upload_photo.html', {'affaire': affaire})

# Create your views here.
from django.shortcuts import get_object_or_404, render
from .models import Essai, Carottage, Sondage, Permeabilite


def essai_detail(request, pk):
    essai = get_object_or_404(Essai, pk=pk)

    # Récupérer les détails spécifiques selon le type d'essai
    details_specifiques = None
    if essai.type_essai == 'CAROTTE':
        details_specifiques = Carottage.objects.filter(essai=essai).first()
    elif essai.type_essai == 'SONDAGE':
        details_specifiques = Sondage.objects.filter(essai=essai).first()
    elif essai.type_essai == 'PERMEA':
        details_specifiques = Permeabilite.objects.filter(essai=essai).first()

    context = {
        'essai': essai,
        'details': details_specifiques
    }
    return render(request, 'suivi_essais/essai_detail.html', context)


def essai_edit(request, pk):
    essai = get_object_or_404(Essai, pk=pk)
    details_specifiques = None
    FormSpecifique = None

    if essai.type_essai == 'CAROTTE':
        details_specifiques = Carottage.objects.filter(essai=essai).first()
        if not details_specifiques:
            details_specifiques = Carottage.objects.create(essai=essai, profondeur=0)
        FormSpecifique = CarottageForm
    elif essai.type_essai == 'SONDAGE':
        details_specifiques = Sondage.objects.filter(essai=essai).first()
        if not details_specifiques:
            details_specifiques = Sondage.objects.create(essai=essai, profondeur=0)
        FormSpecifique = SondageForm
    elif essai.type_essai == 'PERMEA':
        details_specifiques = Permeabilite.objects.filter(essai=essai).first()
        if not details_specifiques:
            details_specifiques = Permeabilite.objects.create(essai=essai, profondeur=0, debit=0)
        FormSpecifique = PermeabiliteForm

    if request.method == 'POST':
        form = EssaiForm(request.POST, instance=essai)
        form_specifique = FormSpecifique(request.POST, instance=details_specifiques)

        if form.is_valid() and form_specifique.is_valid():
            form.save()
            form_specifique.save()
            return redirect('suivi_essais:essai_detail', pk=pk)
    else:
        form = EssaiForm(instance=essai)
        form_specifique = FormSpecifique(instance=details_specifiques)

    return render(request, 'suivi_essais/essai_form.html', {
        'form': form,
        'form_specifique': form_specifique,
        'essai': essai
    })

def import_essais_from_excel(request):
    if request.method == "POST" and request.FILES.get("excel_file"):
        try:
            nb = importer_essais_depuis_excel(request.FILES["excel_file"])
            messages.success(request, f"Importation réussie : {nb} essais ajoutés.")
            return render(request, "suivi_essais/import_excel.html")
        except Exception as e:
            messages.error(request, f"Erreur : {e}")


    return render(request, "suivi_essais/import_excel.html")


