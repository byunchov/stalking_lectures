from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from .helpers.analysis import PlatformDataAnalyser

# from .forms import UploadFileForm

# TODO (sandev): from somewhere import handle_uploaded_file


def test(request):
    return HttpResponse(json.dumps({"message":"API is OK", "status":200, "authorization": False}))


def calculate_mean(request):
    return HttpResponse(f'This is just a test! {request.GET.get("upr", default=None)}')


def central_tendency(request):
    analyser = PlatformDataAnalyser('/Users/ivansandev/Desktop/stalking_lectures/ExampleInputData')

    if request.method == 'GET':
        selector = request.GET.get("upr", default="")
    elif request.method == 'POST':
        selector = request.POST.get("upr", default="")

    data = analyser.calculate_central_tendency(selector)
    return HttpResponse(data);


def all_analysis(request):
    # temporary
    filepath = '/Users/ivansandev/Desktop/stalking_lectures/ExampleInputData'

    analyser = PlatformDataAnalyser(filepath)

    data = analyser.calculate_all()
    return HttpResponse(data);


def upload_file(request):
    from .helpers.file_handling import FileHandler

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/upload/success/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
