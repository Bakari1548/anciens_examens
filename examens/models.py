from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, FileExtensionValidator

class Exam(models.Model):
    class UFR(models.TextChoices):
        DEFAULT = ''
        SET = 'SET'
        SES = 'SES'
        SANTE = 'SANTE'

    class FILIERE(models.TextChoices):
        DEFAULT = ''
        # SET
        LI = 'Licence Informatique'
        LMI = 'Licence Mathematiques Informatique'
        LPC = 'Licence Physique Chimie'
        LSEE = 'Licence en Sciences de l\'Eau et de l\'Environnement'
        # SES
        MIO = 'Management et Informatisé des Organisations'
        MTH = 'Management du tourisme et de l\'hôtellerie'
        LEA = 'Langues Étrangères Appliquées'
        LAC = 'Lettres, Arts et Civilsations'
        SEG = 'Sciences Économiques et Gestion'
        # SANTE
        MDS = 'Médecine et Santé'
        DENT = 'Dentisterie'
        PHARM = 'Pharmacie'

    class MATIERE(models.TextChoices):
        DEFAULT = ''
        MATHS = 'Mathématique'
        PHY = 'Physique'
        CHIMIE = 'Chimie'
        ANG = 'Anglais'
        ESP = 'Espagnol'
        ALG = 'Algorithme'
        POO = 'Programmation orientée objet'
        ASCI = 'Asci'
        DROIT = 'Droit'



    extensions = ['pdf', 'png', 'jpg', 'jpeg', 'webp'] # Les extensions acceptés pour file

    title = models.CharField(max_length=200) # Titre de l'examen
    ufr = models.CharField(max_length=50, choices=UFR.choices, default=UFR.DEFAULT) # UFR de l'examen
    filiere = models.CharField(max_length=500, choices=FILIERE.choices, default=FILIERE.DEFAULT) # Filière
    matiere = models.CharField(choices=MATIERE.choices, max_length=200, default=MATIERE.DEFAULT)
    year = models.IntegerField(validators=[MinValueValidator(2010)], null=True, blank=True) # Année de l'examen
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    ) # Auteur du partage de l'examen
    file = models.FileField(
        upload_to='examens/', 
        validators=[FileExtensionValidator(allowed_extensions=extensions)]
    ) # Fichier PDF ou image
    date_upload = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return self.title