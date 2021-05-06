from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import json

# def upload(request):
#     if request.method == "GET":
#         return render(request, 'upload.html')
#     elif request.method == "POST":
#         return render(request, 'upload_success.html')

def upload(request):
    pass

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['analysis_files']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)
