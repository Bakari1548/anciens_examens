import re
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# --- L'Expression Régulière ---
# Explication du Regex:
# ^ : Début de la chaîne
# [a-zA-Z0-9]+ : Un ou plusieurs caractères alphanumériques (texte ou nombre)
# ([\._-]*[a-zA-Z0-9]+)* : 0 ou plusieurs groupes optionnels de séparateurs (., _, -) suivis de texte/nombre.
#                         (Ceci couvre les emails comme prenom.nom@ ou prenom-nom@)
# @univ-thies\.sn : Le domaine exact. Le point doit être échappé (\.).
# $ : Fin de la chaîne

THIES_EMAIL_REGEX = r'^[a-zA-Z0-9]+([\._-]*[a-zA-Z0-9]+)*@univ-thies\.sn$'


# Définir le validateur en utilisant la classe intégrée RegexValidator
validate_univ_thies_email = RegexValidator(
    regex=THIES_EMAIL_REGEX,
    message=_('Vous devez utiliser votre email universitaire pour vous inscrire (ex: prenom.nom@univ-thies.sn).'),
    code='invalid_univ_thies_email'
)