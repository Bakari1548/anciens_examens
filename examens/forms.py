from django import forms 
from examens.models import Exam


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'ufr', 'filiere', 'matiere', 'year', 'file']
        widgets = { 
            'file': forms.ClearableFileInput(attrs={
                'accept': '.pdf,.png,.jpg,.jpeg,.webp'
            }) 
        }


    UFR_CHOICES = Exam.UFR.choices
    FILIERE_CHOICES = Exam.FILIERE.choices
    MATIERE_CHOICES = Exam.MATIERE.choices

    title = forms.CharField(max_length=150, label="Titre de l'examen")
    ufr = forms.ChoiceField(choices=UFR_CHOICES, label="UFR")
    filiere = forms.ChoiceField(choices=FILIERE_CHOICES, label="Filière")
    matiere = forms.ChoiceField(choices=MATIERE_CHOICES, label="Matière")
    year = forms.IntegerField(min_value=2010, label="Année de l'examen", required=False)
    file = forms.FileField(label="Fichier PDF ou image de l'examen")


class SearchExamForm(forms.Form):
    class Meta:
        fields = ['filiere', 'matiere', 'year']
    
    
    FILIERE_CHOICES = Exam.FILIERE.choices
    MATIERE_CHOICES = Exam.MATIERE.choices

    filiere = forms.ChoiceField(choices=FILIERE_CHOICES, label="Filière", required=False)
    matiere = forms.ChoiceField(choices=MATIERE_CHOICES, label="Matière", required=False)
    year = forms.IntegerField(
        label="Année",
        required=False,
        min_value=2010,
        widget=forms.TextInput(attrs={ 'placeholder': 'minimum: 2010'})
    )
    title_exam = forms.CharField(
        required=False,
        label='Titre de l\'examen',
        widget=forms.TextInput(attrs={ 'placeholder': 'Recherchez par titre...'})
        
    )
    
