"""Files app views"""
import os

import django_tables2 as tables
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

    csv_f = request.GET.get('f')
    # to handle external links contained in csv table
    if csv_f.startswith("https") or csv_f.startswith("http"):
        return HttpResponseRedirect(csv_f)
    df = get_df(csv_f)
    table = get_csv_table(request, df)

    context = {
        'csv_table': table,
        'filename': os.path.basename(csv_f),
        'fpath': csv_f
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
