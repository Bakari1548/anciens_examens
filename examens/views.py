from django.shortcuts import render
from examens.models import Exam
from pdf2image import convert_from_path
import os
from django.conf import settings

def home(request):
    examens = Exam.objects.all()
    return render(request, 'examens/home.html', { 'examens': examens })


def read_exam(request, examen_id):
    examen = Exam.objects.get(id=examen_id)
    
    path_file = examen.file.path
    slug_title = examen.title.replace(" ", "_")
    # par exemple title = Examen Droit ; slug_title = Examen_Droit

    file = examen.file
    images_to_display = []
    if file and file.name.endswith('.pdf'):
        # Convertir le fichier pdf en image avec image2pdf
        images = convert_from_path(path_file)
        # Sauvegarder temporairement les images
        for i, image in enumerate(images):
            # temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', f'{slug_title}_{examen.year}_page_{i+1}.jpg')
            # image.save(temp_path, 'JPEG')
            images_to_display.append(f'/medias/examens/temp/{slug_title}_{examen.year}_page_{i+1}.jpg')
    else:
        # C'est une image déjà stockée dans 'examens/'
        images_to_display.append(examen.file.url)    

  
    context = {
        'examen': examen,
        'images': images_to_display,
        # 'path_file': images_to_display,
    }


    return render(request, 'examens/read_examen.html', context=context)