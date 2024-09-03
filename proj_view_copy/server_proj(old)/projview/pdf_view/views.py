from django.shortcuts import render

def pdf_view(request):
    return render(request, 'pdf_view/viewer.html')


# Create your views here.
