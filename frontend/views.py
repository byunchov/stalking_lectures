from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
# from django.http import HttpResponse, HttpResponseRedirect
import json
import os
import shutil


@login_required
def home_view(request):
    return render(request, 'frontend/pages/home.html', {})


@login_required
def analysis_list_view(request,):
    context = {}
    context['range'] = range(1,16)

    return render(request, 'frontend/pages/analysis.html', context)


@login_required
def analysis_main_view(request, upload_id):
    context = {}
    context['upload_id'] = upload_id

    return render(request, 'frontend/pages/analysis_item.html', context)


@login_required
def analysis_spread_view(request, upload_id):
    context = {}
    context['upload_id'] = upload_id

    return render(request, 'frontend/pages/spread.html', context)


def upload(request, user_id):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['analysis_files']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, str(user_id)))
        file_path = os.path.join(settings.MEDIA_ROOT, str(user_id))
        try:
            os.makedirs(file_path)
        except FileExistsError:
            # TODO
            # shutil.rmtree(file_path) # force deletes directory (even if not empty)
            # os.removedirs(os.path.join(settings.MEDIA_ROOT, str(user_id)))
            # os.makedirs(file_path)
            pass
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)
