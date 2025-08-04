from django.shortcuts import render

def home(request):
    return render(request, 'examens/home.html')