from django.shortcuts import render
from django.http import HttpResponse
import json
from .helpers.analysis import PlatformDataAnalyser


def file_upload():
    analyser = PlatformDataAnalyser('./uploads/course_{id}')

def calculate_mean(request):
    
    return HttpResponse(f'This is just a test! {request.GET.get("upr", default=None)}')

def central_tendency(request):

    print(request.user)
    analyser = PlatformDataAnalyser('/home/bobiyu/Documents/UNI/ПТС/test_folder/files')

    if request.method == 'GET':
        selector = request.GET.get("upr", default="")
    elif request.method == 'POST':
        selector = request.POST.get("upr", default="")

    data = analyser.calculate_central_tendency(selector)
    return HttpResponse(data)