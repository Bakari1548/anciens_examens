import os
from django.shortcuts import render, redirect
from examens.models import Exam
from django.db.models import Q
from examens.forms import ExamForm, SearchExamForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from pdf2image import convert_from_path
from unidecode import unidecode


def home(request):
    examens = Exam.objects.all().order_by('-date_upload')

    # Crée une instance du formulaire, pré-remplie avec les données GET
    form = SearchExamForm(request.GET)

    if form.is_valid():
        year_filter = form.cleaned_data.get('year')
        matiere_filter = form.cleaned_data.get('matiere')
        filiere_filter = form.cleaned_data.get('filiere')
        title_exam_filter = form.cleaned_data.get('title_exam')
        
        # Gestion du filtrage des examens
        if year_filter or matiere_filter or filiere_filter:
            if matiere_filter:
                examens = Exam.objects.filter(matiere=matiere_filter).order_by('-date_upload')
            
            if filiere_filter:
                examens = Exam.objects.filter(filiere=filiere_filter).order_by('-date_upload')
            
            if year_filter:
                examens = Exam.objects.filter(year=year_filter).order_by('-date_upload')

            if year_filter and matiere_filter:
                examens = Exam.objects.filter(
                    Q(year=year_filter) &
                    Q(matiere=matiere_filter)
                ).order_by('-date_upload')
            
            if matiere_filter and filiere_filter:
                examens = Exam.objects.filter(
                    Q(matiere=matiere_filter) &
                    Q(filiere=filiere_filter)
                ).order_by('-date_upload')
            
            if year_filter and filiere_filter:
                examens = Exam.objects.filter(
                    Q(year=year_filter) &
                    Q(filiere=filiere_filter)
                ).order_by('-date_upload')
                
            if year_filter and filiere_filter and matiere_filter:
                examens = Exam.objects.filter(
                    Q(year=year_filter) &
                    Q(filiere=filiere_filter) &
                    Q(matiere=matiere_filter)
                ).order_by('-date_upload')
        
        # rechercher en tapant le titre de l'examen
        if title_exam_filter:
            examens = Exam.objects.filter(title=title_exam_filter).order_by('-date_upload')
        
        # On recupere les résultats pour une page individuelle et on specifie les nombres d'instances à affiche "3"
        paginator = Paginator(examens, 6)
        # Recuperer le numero de page dans l'url
        page_number = request.GET.get('page')
        # Recuperer l'objet (liste ou QuerySet) représentant la page sur laquelle nous sommes
        page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        # 'examens': examens,
        'page_obj': page_obj,
    }


    return render(request, 'examens/home.html', context)


def read_exam(request, examen_id):
    examen = Exam.objects.get(id=examen_id)
    
    path_file = examen.file.path
    slug_title = unidecode(examen.title.replace(" ", "_"))
    print(slug_title)
    
    # par exemple title = Examen Mathématiques ; slug_title = Examen_Mathematiques

    file = examen.file
    images_to_display = []
    if file and file.name.endswith('.pdf'):
        temp_dir_name = f'temp/{slug_title}_{examen.year or ""}'
        temp_dir_path = os.path.join(settings.MEDIA_ROOT, temp_dir_name)
        os.makedirs(temp_dir_path, exist_ok=True)

        # Convertir seulement la premiere du fichier PDF avec image2pdf
        images = convert_from_path(path_file, first_page=1, last_page=1)

        # Sauvegarder l'image de la premiere page
        if images: # Pour verifier si la liste n'est pas vide
            image = images[0]
            image_name = f'{slug_title}.jpg'
            image_path = os.path.join(temp_dir_path, image_name)

            # Sauvegarde l'image sur le disque
            # image.save(image_path, 'JPEG')

            # Ajoute l'URL de l'image à la liste pour le template
            images_to_display.append(os.path.join(settings.MEDIA_URL, temp_dir_name, image_name).replace('\\', '/'))

    else:
        # C'est une image déjà stockée dans 'examens/'
        images_to_display.append(examen.file.url)    

    print(images_to_display)
  
    context = {
        'examen': examen,
        'images': images_to_display,
        # 'path_file': images_to_display,
    }
    
    context = { 'examen': examen }
    return render(request, 'examens/read_examen.html', context=context)


@login_required  # pour partager un examen il faut se connecter 
def post_exam(request):
    if request.method == 'POST':
        print("FILES:", request.FILES)  # Vérifiez si le fichier est présent
        # print("POST:", request.POST)
        form = ExamForm(request.POST, request.FILES)
        if form.is_valid():
            # sauvegarder les donnees entrees sans l'envoyer
            examen = form.save(commit=False)
            # lier l'auteur et l'examen à partager
            examen.author = request.user
            # print(examen.file)
            # sauvegarder definitivement les donnees de examen
            examen.save()
            # apres sauvegarde rediriger vers une page qui detaille l'examen partage
            return redirect('read_exam', examen.id)
    else:
        form = ExamForm()


    return render(request,
        'examens/post_exam.html',
        context={ 'form': form }
    )


def regle(request):

    return render(request, 'examens/regles.html')

