"""Files app views"""
import csv
import io
import os

import django_tables2 as tables
import pandas as pd
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from files.forms import UploadFileForm
from files.models import File
from files.tables import FilesTable
from files.utils.get_ext import get_ext
from files.utils.get_table import get_table_from_headers
from files.utils.info_upload import info_upload


@csrf_protect
def upload_file(request):
    """Handles file upload"""

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        user = request.user
        file = request.FILES["file"]
        fname = file.name
        is_csv = get_ext(fname) == ".csv"

        # Only {'.csv'} files allowed
        if form.is_valid() and is_csv:
            # searches db among user's files for a match
            prev_file = File.objects \
                .filter(file_name=fname).all() \
                .filter(user=user).first()
            if not prev_file:
                f = file.read().decode('utf-8')
                reader = csv.DictReader(io.StringIO(f))
                fieldnames = ", ".join(reader.fieldnames)
                new = File(
                    file=file,
                    file_name=fname,
                    headers=fieldnames,
                    user=user
                )
                new.save()
            else:
                # deletes existing file
                prev_file_path = prev_file.file.path
                os.remove(prev_file_path)
                prev_file.delete()
                # prepares file record stamped as 'reviewed'
                reviewed = File(
                    file=file,
                    file_name=fname,
                    user=user,
                    status="reviewed"
                )
                # uploads a new reviewed file version
                reviewed.save()

            info_upload(request, fname, is_csv)
            return HttpResponseRedirect("/files_table/")

        else:
            info_upload(request, fname, is_csv)
    else:
        # An empty form
        form = UploadFileForm()

    return render(request, "files/upload.html", {"form": form})


def csv_table(request):
    """Handles .csv file view as a table"""

    csv_f = request.GET.get('f')

    if csv_f.startswith("https"):
        return HttpResponseRedirect(csv_f)

    filename = os.path.basename(csv_f)
    df = pd.read_csv(csv_f)
    headers = []
    for col in df.columns:
        headers.append(col)
    dynamic_table = get_table_from_headers(headers)
    table = dynamic_table(
        data=df.to_dict("records"),
        template_name="django_tables2/bootstrap5.html"
    )
    table.paginate(page=request.GET.get("page", 1), per_page=25)

    context = {'csv_table': table, 'filename': filename, 'fpath': csv_f}

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
