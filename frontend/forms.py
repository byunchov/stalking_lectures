from django import forms
from api.models import Upload
from api.helpers.application_field_content import selectin_list_for_application_field as appl_field_sl


class UploadForm(forms.Form):
    file_field_attrs = { 'name': 'analysis_files', 'multiple': True, 'accept': '.xls, .xlsx, .ods, .odf ,.odt, .csv, .zip'}

    platform_name = forms.CharField(max_length=255, label='Име на платформа', required=True)
    platform_type = forms.CharField(max_length=255, label='Тип на платформа', required=True)
    platform_url = forms.URLField(label='Адрес на платформа', required=True)
    course_name = forms.CharField(max_length=255, label='Дисциплина', required=True)
    application_field = forms.CharField(label='Област на приложение', max_length=255, widget=forms.Select(choices=appl_field_sl))
    files = forms.FileField(label='Файлове за анализ', widget=forms.ClearableFileInput(attrs=file_field_attrs), required=True)


class UploadModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(UploadModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Upload
        exclude = ('date_added',)