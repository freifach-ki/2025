"""
QR-Code Generator fuer das Werbeplakat Kurs 4001.
Ziel anpassen: QR_TARGET unten aendern, dann ausfuehren:  python make_qr.py
Erzeugt qr-4001.svg (scharf fuer Druck, beliebig skalierbar).
"""
import qrcode
import qrcode.image.svg

# >>> HIER DAS ECHTE ANMELDE-ZIEL EINTRAGEN <<<
# Beispiele:
#   "https://www.bbw.ch/freifaecher/anmeldung"        (Online-Formular)
#   "mailto:vorname.nachname@bbw.ch?subject=Anmeldung%20Kurs%204001%20KI&body=Ich%20melde%20mich%20fuer%20den%20Freifachkurs%20KI%20(4001)%20an.%20Name%3A%20___%20Klasse%3A%20___"
QR_TARGET = "mailto:vorname.nachname@bbw.ch?subject=Anmeldung%20Kurs%204001%20-%20KI%20fuer%20Schule%20und%20Beruf&body=Ich%20melde%20mich%20verbindlich%20fuer%20den%20Freifachkurs%20KI%20(4001)%20an.%0AName%3A%20%0AKlasse%3A%20"

factory = qrcode.image.svg.SvgPathImage
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
qr.add_data(QR_TARGET)
qr.make(fit=True)
img = qr.make_image(image_factory=factory)
img.save("qr-4001.svg")
print("OK -> qr-4001.svg")
print("Ziel:", QR_TARGET)
