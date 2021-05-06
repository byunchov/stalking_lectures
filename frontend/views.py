from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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
