from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from .helpers.analysis import PlatformDataAnalyser
from django.conf import settings
import os

# from .forms import UploadFileForm

def test(request):
    return HttpResponse(json.dumps({"message":"API is OK", "status":200, "authorization": False}))

def file_upload():
    analyser = PlatformDataAnalyser('./uploads/course_{id}')

def calculate_mean(request):
    return HttpResponse(f'This is just a test! {request.GET.get("upr", default=None)}')


def central_tendency(request):
    analyser = PlatformDataAnalyser('/home/bobiyu/Documents/UNI/ПТС/test_folder/files')

    if request.method == 'GET':
        selector = request.GET.get("upr", default="")
    elif request.method == 'POST':
        selector = request.POST.get("upr", default="")

    data = analyser.calculate_central_tendency(selector)
    return HttpResponse(data);


def all_analysis(request, user_id):
    # temporary
    # filepath = '/Users/ivansandev/Desktop/stalking_lectures/ExampleInputData'
    filepath = os.path.join(settings.MEDIA_ROOT, str(user_id))

    analyser = PlatformDataAnalyser(filepath)

    data = analyser.calculate_all()
    return HttpResponse(data);


# def upload_file(request):
#     from .helpers.file_handling import FileHandler

#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             #handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/upload/success/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})
