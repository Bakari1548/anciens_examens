from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, FileExtensionValidator

class Exam(models.Model):

    SES = 'SES'
    SET = 'SET'
    SANTE = 'SANTE' 
    

    UFR_CHOICES = (
        (SET, 'Set'),
        (SES, 'Ses'),
        (SANTE, 'Santé'),
    )

    BRANCH_CHOICES = (
        # SET
        ('LI', 'Licence Informatique'),
        ('LMI', 'Licence Mathematiques Informatique'),
        ('LPC', 'Licence Physique Chimie'),
        ('LSEE', 'Licence en Sciences de l\'Eau et de l\'Environnement'),
        # SES
        ('MIO', 'Management et Informatisé des Organisations'),
        ('MTH', 'Management du tourisme et de l\'hôtellerie'),
        ('LEA', 'Langues Étrangères Appliquées'),
        ('LAC', 'Lettres, Arts et Civilsations'),
        ('SEG', 'Sciences Économiques et Gestion'),
        # SANTE
        ('MDS', 'Médecine et Santé'),
        ('DENT', 'Dentisterie'),
        ('PHARM', 'Pharmacie'),
    )


    extensions = ['pdf', 'png', 'jpg', 'jpeg', 'webp'] # Les extensions acceptés pour le file

    title = models.CharField(max_length=200) # Titre de l'examen
    ufr = models.CharField(max_length=50, choices=UFR_CHOICES) # UFR de l'examen
    branch = models.CharField(max_length=500, choices=BRANCH_CHOICES) # Filière
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
    
    def pdf_to_image(self):
        if self.file and self.file.name.endswith('.pdf'):
            # PDF file detected
            print("Doc PDF detecte")
        else:
            print("Doc PDF non detecte")
