from django.urls import reverse
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.colors import Color
from reportlab.pdfbase.acroform import orientations
from reportlab.pdfgen import canvas
import qrcode
from reportlab.lib.utils import ImageReader
import io
import tempfile

def generate_etiquette_pdfs_for_essais(essais_queryset):
    """
    Génère un PDF d'étiquettes (format A5) pour une liste d'essais.
    Retourne le chemin du fichier PDF généré.
    """
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf').name
    c = canvas.Canvas(temp_path, pagesize=A5)

    for essai in essais_queryset:
        render_etiquette_by_type(c, essai)
        c.showPage()

    c.save()
    return temp_path

def render_etiquette_by_type(c, essai):
    """
    Appelle la fonction de rendu en fonction du type d'essai.
    """
    type_essai = getattr(essai, 'type_essai', '').lower()
    print(f"[DEBUG] Étiquette pour essai ID {essai.identifiant} — type détecté : {type_essai}")

    if type_essai == 'carotte':
        render_etiquette_carottage(c, essai)
    elif type_essai == 'sondage':
        render_etiquette_sondage(c, essai)
    elif type_essai == 'permea':
        render_etiquette_permeabilite(c, essai)
    else:
        render_etiquette_generique(c, essai)

def render_etiquette_carottage(c, essai):
    """
    Rend une étiquette PDF A5 paysage pour un essai de type carottage.
    """
    c.setPageSize(landscape(A5))  # Format paysage

    # Marges de base
    width, height = landscape(A5)
    center_x = width / 2

    # Récupération des données
    ref_dossier = getattr(essai.affaire, 'code_affaire', '')
    ref_ems = getattr(essai, 'os_no_engagement', '')
    code_ems = getattr(essai, 'os_no', '')
    #adresse = f"{getattr(essai.affaire, 'ville', '').upper()} - {getattr(essai.affaire, 'rue', '')}"
    adresse = f"{getattr(essai, 'ville', '').upper()} - {getattr(essai, 'rue', '')}"
    identifiant = essai.identifiant

    print(f"[DEBUG] Impression Étiquette pour essai ID {identifiant} — Ville : {adresse}")

    # Définitino du gris sombre
    gris_sombre_rgb = (70, 70, 70)
    gris_sombre_color = Color(*[x / 255 for x in gris_sombre_rgb])

    # Bordure
    c.setStrokeColor(gris_sombre_color)
    c.setLineWidth(2)
    margin = 10
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin, stroke=1, fill=0)

    # Référence dossier + Ref. EMS (en-tête)
    c.setFont("Helvetica", 16)
    c.drawString(30, height - 40, ref_dossier)
    c.drawRightString(width - 30, height - 40, f"Ref. EMS: {ref_ems}")

    # Code EMS (gros, centré)
    #c.setFont("Helvetica-Bold", 28)
    #c.drawCentredString(center_x, height - 110, code_ems)

    # Adresse (majuscules, centrée)
    c.setFont("Helvetica", 16)
    c.drawCentredString(center_x, height - 100, adresse)


    # Code opération (centré)
    c.setFillColor(gris_sombre_color)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(center_x, height - 210, identifiant)

    # URL vers essai_detail (relative)
    relative_url = reverse("suivi_essais:essai_detail", kwargs={"pk": essai.id})

    # URL absolue complète
    base_url = "http://skarottbuch.sirs.fr:8000"
    full_url = f"{base_url}{relative_url}"

    print(f"[DEBUG] QR code URL = {full_url}")

    # Génération du QR code
    # QR code avec couleur
    #qr = qrcode.QRCode(border=1)
    #qr.add_data(full_url)
    #qr.make(fit=True)
    #img = qr.make_image(fill_color=gris_sombre_rgb, back_color="white")

    #qr = qrcode.make(full_url)
    #buffer = io.BytesIO()
    #qr.save(buffer, format="PNG")
    #buffer.seek(0)
    #qr_image = ImageReader(buffer)

    #qr_size = 120
    #qr_x = center_x - qr_size / 2
    #qr_y = 40
    #c.drawImage(qr_image, qr_x, qr_y, width=qr_size, height=qr_size)

    #
    # QR code (avec même couleur)
    relative_url = reverse("suivi_essais:essai_detail", kwargs={"pk": essai.id})
    full_url = f"http://skarottbuch.sirs.fr:8000{relative_url}"
    print(f"[DEBUG] QR SONDAGE = {full_url}")

    qr = qrcode.QRCode(border=1)
    qr.add_data(full_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=gris_sombre_rgb, back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    qr_image = ImageReader(buffer)
    qr_size = 120
    qr_x = center_x - qr_size / 2
    qr_y = 40
    c.drawImage(qr_image, qr_x, qr_y, width=qr_size, height=qr_size)




    # ➕ QR Code (identifiant)
    #qr = qrcode.make(identifiant)
    #buffer = io.BytesIO()
    #qr.save(buffer, format="PNG")
    #buffer.seek(0)
    #qr_image = ImageReader(buffer)

    #qr_size = 120  # taille du carré QR (en points ≈ 4,2 cm)
    #qr_x = center_x - qr_size / 2
    #qr_y = 30  # distance du bas de la page

    #c.drawImage(qr_image, qr_x, qr_y, width=qr_size, height=qr_size)


def render_etiquette_sondage(c, essai):
    from reportlab.lib.colors import Color

    c.setPageSize(landscape(A5))
    width, height = landscape(A5)
    center_x = width / 2

    ref_dossier = getattr(essai.affaire, 'code_affaire', '')
    ref_ems = getattr(essai, 'os_no_engagement', '')
    adresse = f"{getattr(essai, 'ville', '').upper()} - {getattr(essai, 'rue', '')}"
    identifiant = essai.identifiant

    print(f"[DEBUG] Impression Étiquette SONDAGE ID {identifiant} — Adresse : {adresse}")

    # Définition couleur BRUN
    brun_rgb = (139, 69, 19)
    brun_color = Color(*[x / 255 for x in brun_rgb])
    c.setStrokeColor(brun_color)

    # Dessin de la bordure
    margin = 10  # marge depuis le bord
    c.setLineWidth(2)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin, stroke=1, fill=0)

    c.setFont("Helvetica", 16)
    c.drawString(30, height - 40, ref_dossier)
    c.drawRightString(width - 30, height - 40, f"Ref. EMS: {ref_ems}")
    c.drawCentredString(center_x, height - 100, adresse)

    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(Color(*[x/255 for x in brun_rgb]))
    c.drawCentredString(center_x, height - 210, identifiant)
    c.setFillColorRGB(0, 0, 0)  # reset

    # QR code (avec même couleur)
    relative_url = reverse("suivi_essais:essai_detail", kwargs={"pk": essai.id})
    full_url = f"http://skarottbuch.sirs.fr:8000{relative_url}"
    print(f"[DEBUG] QR SONDAGE = {full_url}")

    qr = qrcode.QRCode(border=1)
    qr.add_data(full_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=brun_rgb, back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    qr_image = ImageReader(buffer)
    qr_size = 120
    qr_x = center_x - qr_size / 2
    qr_y = 40
    c.drawImage(qr_image, qr_x, qr_y, width=qr_size, height=qr_size)

def render_etiquette_permeabilite(c, essai):
    from reportlab.lib.colors import Color

    c.setPageSize(landscape(A5))
    width, height = landscape(A5)
    center_x = width / 2

    ref_dossier = getattr(essai.affaire, 'code_affaire', '')
    ref_ems = getattr(essai, 'os_no_engagement', '')
    adresse = f"{getattr(essai, 'ville', '').upper()} - {getattr(essai, 'rue', '')}"
    identifiant = essai.identifiant

    print(f"[DEBUG] Impression Étiquette PERMÉA ID {identifiant} — Adresse : {adresse}")

    bleu_rgb = (0, 102, 204)
    bleu_color = Color(*[x / 255 for x in bleu_rgb])
    c.setStrokeColor(bleu_color)

    margin = 10
    c.setLineWidth(2)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin, stroke=1, fill=0)

    c.setFont("Helvetica", 16)
    c.drawString(30, height - 40, ref_dossier)
    c.drawRightString(width - 30, height - 40, f"Ref. EMS: {ref_ems}")
    c.drawCentredString(center_x, height - 100, adresse)

    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(Color(*[x/255 for x in bleu_rgb]))
    c.drawCentredString(center_x, height - 210, identifiant)
    c.setFillColorRGB(0, 0, 0)  # reset

    # QR code (avec même couleur)
    relative_url = reverse("suivi_essais:essai_detail", kwargs={"pk": essai.id})
    full_url = f"http://skarottbuch.sirs.fr:8000{relative_url}"
    print(f"[DEBUG] QR PERMÉA = {full_url}")

    qr = qrcode.QRCode(border=1)
    qr.add_data(full_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=bleu_rgb, back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    qr_image = ImageReader(buffer)
    qr_size = 120
    qr_x = center_x - qr_size / 2
    qr_y = 40
    c.drawImage(qr_image, qr_x, qr_y, width=qr_size, height=qr_size)

def render_etiquette_generique(c, essai):
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 550, f"Essai Générique : {essai.identifiant} — {essai.libelle}")
