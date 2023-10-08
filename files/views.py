"""Files app views"""
import os

import django_tables2 as tables
import pandas as pd
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from files.forms import ColumnRowsForm, UploadFileForm
from files.handlers.handle_filter_by_rows import handle_filter_by_rows
from files.handlers.handle_uploaded_file import handle_uploaded_file
from files.models import File
from files.tables import FilesTable
from files.utils.df_sort import df_sort
from files.utils.get_csv_table import get_csv_table
from files.utils.get_df import get_df


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


@method_decorator(csrf_protect, 'post')
class FilesTableView(tables.SingleTableView):
    """Provides table view for uploaded files"""

    table_class = FilesTable
    template_name = "files/uploaded_files.html"

    def post(self, request, *args, **kwargs):
        """Allows post-method for a view"""

        return super().get(self, *args, *kwargs)

    def get_queryset(self):
        """Outputs current user files"""

        # deletes selected File table objects
        if self.request.method == "POST":
            pks = self.request.POST.getlist("delete")
            selected_files = File.objects.filter(pk__in=pks)
            selected_files.delete()

        return File.objects \
            .filter(user=self.request.user) \
            .order_by("-date")


def csv_table(request):
    """Handles .csv file view as a table"""

    sort = request.GET.get("sort")
    user = request.user
    fpath = request.GET.get('req')
    fname = os.path.basename(fpath)
    customized_path = f"media/user_{user.id}/{'customized.' + fname}"

    # to handle external links contained in csv table
    if fpath.startswith("http") or fpath.startswith("https"):
        return HttpResponseRedirect(fpath)

    column_rows_form = ColumnRowsForm(request.POST)

    request.session['filename'] = fname
    request.session["customized_path"] = customized_path
    request.session["as_link"] = []

    res = handle_filter_by_rows(
        request=request,
        path=fpath,
        sort=sort,
        form=column_rows_form
    )
    if not res[0]:
        return HttpResponseRedirect("/customized/")
    df = res[1]

    table = get_csv_table(request, df, links=None)

    context = {
        "filename": fname,
        "filepath": fpath,
        "table": table,
        "column_rows_form": column_rows_form
    }

    return render(request, "files/csv_table.html", context)


@csrf_protect
def customize_csv(request):
    """Customize .csv file configuration"""

    sort = request.GET.get("sort")
    user = request.user
    headers = request.GET.get('req')
    file = File.objects.get(user=user, headers=headers)
    fname = file.file_name
    fpath = file.file
    customized_path = f"media/user_{user.id}/{'customized.' + fname}"

    if request.method == "POST":
        include_columns = request.POST.getlist("include")
        as_link = request.POST.getlist("as_link")
        if not include_columns:
            return HttpResponseRedirect("/files_table/")

        df = get_df(path=fpath, usecols=include_columns)
        df.to_csv(path_or_buf=customized_path, encoding='utf-8', index=False)

        request.session['filename'] = fname
        request.session["customized_path"] = customized_path
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

    return render(request, "files/csv_table_customize.html", context)


def customized(request):
    """Customized .csv preview"""

    sort = request.GET.get("sort")
    fname = request.session['filename']
    fpath = request.session['customized_path']
    as_link = request.session["as_link"]

    column_rows_form = ColumnRowsForm(request.POST)

    res = handle_filter_by_rows(
        request=request,
        path=fpath,
        sort=sort,
        form=column_rows_form
    )
    if not res[0]:
        return HttpResponseRedirect("/customized/")
    df = res[1]

    table = get_csv_table(request, df, links=as_link)

    context = {
        "filename": fname,
        "filepath": fpath,
        "table": table,
        "column_rows_form": column_rows_form
    }

    return render(request, "files/csv_table.html", context)
