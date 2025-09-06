from django import forms 
from examens.models import Exam


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'ufr', 'branch', 'year', 'file']
        widgets = { 
            'file': forms.ClearableFileInput(attrs={
                'accept': '.pdf,.png,.jpg,.jpeg,.webp'
            }) 
        }


    UFR_CHOICES = Exam.UFR.choices
    FILIERE_CHOICES = Exam.FILIERE.choices

    title = forms.CharField(max_length=150, label="Titre de l'examen")
    ufr = forms.ChoiceField(choices=UFR_CHOICES, label="UFR")
    branch = forms.ChoiceField(choices=FILIERE_CHOICES, label="Filière")
    year = forms.IntegerField(min_value=2010, label="Année de l'examen", required=False)
    file = forms.FileField(label="Fichier PDF ou image de l'examen")

