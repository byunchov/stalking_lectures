from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import UploadForm, UpdateForm
from api.models import Upload, CorrelationAnalysis
from api.helpers.analysis import PlatformDataAnalyser
from api.helpers.analysis_exceptions import NoActivityLogFile, NoStudentResultsFile, InvalidDataInFile
from django.forms import modelform_factory, modelformset_factory

# from django.http import HttpResponse, HttpResponseRedirect
import json
import os
import shutil


def format_upload_path(request):
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f'user_{request.user.id}/{ts}'


def post_upload_handler(path):
    try:
        # SAFER WAY (delete file by file)
        # # delete all uploads
        # for file in request.FILES.getlist('files'):
        #     fs.delete(file.name)
        # # delete timestamp directory
        # fs_def = FileSystemStorage(location=settings.MEDIA_ROOT)
        # fs_def.delete(upload_path)
        # # delete user_id directory
        # fs_def.delete(upload_path[0:upload_path.rfind('/')])

        # SIMPLER (deletes all files for selected user)
        shutil.rmtree(path[0:path.rfind('/')])
    except:
        print("DBG: Cannot delete files")


@login_required
def home_view(request):
    # TODO
    # Move this section to api.views -> upload
    context = {}

    if request.method == 'POST':
        # verify form
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_path = os.path.join(
                settings.MEDIA_ROOT, format_upload_path(request))
            fs = FileSystemStorage(location=upload_path)

            # save files to local storage
            for upload in request.FILES.getlist('files'):
                fs.save(upload.name, upload)

            # TODO
            # pass f_data fields to Upload model and save it to DB
            f_data = form.cleaned_data
            del f_data['files']

            try:
                pda = PlatformDataAnalyser(upload_path)
                pda.save_all()

                upload = Upload(user=request.user, **f_data)
                upload.save()

                corr = CorrelationAnalysis(
                    upload=upload, correlation_data=pda.correlation_data, freq_distrib=pda.corr_freq_distrib)
                corr.save()
                
                # Clear uploaded files
                post_upload_handler(upload_path)

                # if everything went as expected, redirect to upload overview page
                return redirect('analysis_item', upload.pk)

            except NoStudentResultsFile:
                # Retutn response to user for the error
                context['response'] = {'status': 'danger', 'msg': {
                    'heading': 'Невалидни данни', 'content': 'Качените файлове не съдържат списък с оценки на студенти!'}}
            
            except NoActivityLogFile:
                # Retutn response to user for the error
                context['response'] = {'status': 'danger', 'msg': {
                    'heading': 'Невалидни данни', 'content': 'Качените файлове не съдържат списък с активност на студенти!'}}
            
            except InvalidDataInFile:
                # Retutn response to user for the error
                context['response'] = {'status': 'danger', 'msg': {
                    'heading': 'Невалидни данни', 'content': 'Качените файлове не съдържат необходимите данни за анализ!'}}                

            finally:
                # Clear uploaded files
                post_upload_handler(upload_path)
                # Returna input form data, so the user doesn't need to enter it again
                # context['form'] = form
   
        else:
             context['response'] = {'status': 'danger', 'msg': {
                    'heading': 'Невалидни данни', 'content': 'Проверете попълнените полета и опитайте отново.'}}

    else:
        # Return balnk form
        form = UploadForm()

    context['form'] = form
    return render(request, 'frontend/pages/home.html', context)


@login_required
def analysis_list_view(request):
    context = {}
    context['uploaded_analysis'] = Upload.objects.filter(
        user=request.user).order_by('-date_added')

    return render(request, 'frontend/pages/analysis.html', context)


@login_required
def analysis_main_view(request, upload_id):
    context = {}
    item = Upload.objects.get(pk=upload_id)
    context['item'] = item

    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=item)

        if form.is_valid():
            # f_data = form.cleaned_data
            # Upload.objects.update(pk=upload_id, **f_data)
            # item.objects.update(pk=upload_id, **f_data)
            form.save()
            context['response'] = {'status': 'success',
                                   'msg': { 'content': 'Информацията е обовена успешно!' } }
        else:
            context['response'] = {
                'status': 'danger', 'msg': { 'content': 'Възникна грешка! Моля, проверете полетата и опитайте отново!' }}

    else:
        form = UpdateForm(instance=item)

    context['form'] = form

    return render(request, 'frontend/pages/analysis_item.html', context)


@login_required
def analysis_freq_dist_view(request, upload_id):
    context = {}
    context['upload_id'] = upload_id

    return render(request, 'frontend/pages/freq_dist.html', context)


@login_required
def analysis_trend_view(request, upload_id):
    context = {}
    context['upload_id'] = upload_id

    return render(request, 'frontend/pages/trend.html', context)


@login_required
def analysis_spread_view(request, upload_id):
    context = {}
    context['upload_id'] = upload_id

    return render(request, 'frontend/pages/spread.html', context)


@login_required
def analysis_correlations_view(request, upload_id):
    context = {}
    context['upload_id'] = upload_id
    context['item'] = Upload.objects.get(pk=upload_id)

    return render(request, 'frontend/pages/correlations.html', context)


def upload(request, user_id):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['analysis_files']
        print(uploaded_file.name)
        file_path = os.path.join(settings.MEDIA_ROOT, str(user_id))
        fs = FileSystemStorage(location=file_path)
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
