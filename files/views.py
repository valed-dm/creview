"""Files app views"""
import os

import django_tables2 as tables
import pandas as pd
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from files.forms import UploadFileForm
from files.handlers.handle_uploaded_file import handle_uploaded_file
from files.models import File
from files.tables import FilesTable
from files.utils.get_csv_table import get_csv_table
from files.utils.get_df import get_df
from files.utils.df_sort import df_sort



@csrf_protect
def upload_file(request):
    """Handles file upload"""

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if handle_uploaded_file(request):
                return HttpResponseRedirect("/files_table/")
    else:
        form = UploadFileForm()

    return render(request, "files/upload.html", {"form": form})


def csv_table(request):
    """Handles .csv file view as a table"""

    csv_file_path = request.GET.get('req')
    sort = request.GET.get("sort")
    # to handle external links contained in csv table
    if csv_file_path.startswith("http") or csv_file_path.startswith("https"):
        return HttpResponseRedirect(csv_file_path)
    df = get_df(path=csv_file_path, sort=sort)
    table = get_csv_table(request, df, links=None)
    context = {
        'filename': os.path.basename(csv_file_path),
        'filepath': csv_file_path,
        'table': table,
    }

    return render(request, "files/csv_table.html", context)


@csrf_protect
def set_csv_preview(request):
    """Handles .csv file customized preview configuration"""

    headers = request.GET.get('req')
    sort = request.GET.get("sort")
    file = File.objects.get(headers=headers)
    fname = file.file_name
    fpath = file.file

    if request.method == "POST":
        include_columns = request.POST.getlist("include")
        as_link = request.POST.getlist("as_link")
        df = get_df(path=fpath, usecols=include_columns)
        customized_path = f"media/{'customized.' + fname}"
        df.to_csv(path_or_buf=customized_path, encoding='utf-8', index=False)
        request.session['filename'] = fname
        request.session["filepath"] = customized_path
        request.session["as_link"] = as_link

        return HttpResponseRedirect("/customized/")

    hds = headers.split(", ")
    checkboxes = [0 for h in hds]
    data = {
        "columns": hds,
        "include": checkboxes,
        "as_link": checkboxes
    }
    df = pd.DataFrame(data)
    if sort:
        df = df_sort(df=df, sort=sort)
    table = get_csv_table(request, df, links=None)
    context = {
        "filename": fname,
        "filepath": fpath,
        "table": table
    }

    return render(request, "files/set_csv_preview.html", context)


def customized_preview(request):
    """Customized .csv preview"""

    sort = request.GET.get("sort")
    fname = request.session['filename']
    fpath = request.session['filepath']
    as_link = request.session["as_link"]
    df = get_df(path=fpath, sort=sort)
    table = get_csv_table(request, df, links=as_link)

    context = {
        "filename": fname,
        "filepath": fpath,
        "table": table
    }

    return render(request, "files/csv_table.html", context)


@method_decorator(csrf_protect, 'post')
class FilesTableView(tables.SingleTableView):
    """Provides table view for uploaded files"""

    table_class = FilesTable
    template_name = "files/files_table.html"

    def post(self, request, *args, **kwargs):
        """Allows post-method for a view"""

        return super().get(self, *args, *kwargs)

    def get_queryset(self):
        """Outputs current user files"""

        # deletes uploaded files from user's media folder on request
        if self.request.method == "POST":
            pks = self.request.POST.getlist("delete")
            selected_files = File.objects.filter(pk__in=pks)
            selected_files.delete()

        return File.objects \
            .filter(user=self.request.user) \
            .order_by("-date")
