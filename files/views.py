"""Files app views"""

import os

import django_tables2 as tables
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView

from files.forms import UploadFileForm
from files.models import File
from files.tables import FilesTable
from files.utils.get_ext import get_ext
from files.utils.info_upload import info_upload


@csrf_protect
def upload_file(request):
    """Handle file upload"""

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        user = request.user
        file = request.FILES["file"]
        fname = request.FILES['file'].name
        file_is_py = get_ext(fname) == ".py"

        # Only {'.py'} files allowed
        if form.is_valid() and file_is_py:
            # searches db among user's files for a match
            prev_file = File.objects \
                .filter(file_name=fname).all() \
                .filter(user=user).first()
            if not prev_file:
                new = File(
                    file=file,
                    file_name=fname,
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

            info_upload(request, fname, file_is_py)
            return HttpResponseRedirect("/files_table/")

        else:
            info_upload(request, fname, file_is_py)
    else:
        # An empty form
        form = UploadFileForm()

    return render(request, "files/upload.html", {"form": form})


class FilesTableView(tables.SingleTableView):
    """Provides uploaded files table view """

    table_class = FilesTable
    template_name = "files/files_table.html"

    def get_queryset(self):
        """Filters output for user's files"""

        return File.objects \
            .filter(user=self.request.user) \
            .order_by("-date")


class ReportView(ListView):
    """Provides report view"""

    template_name = "files/report.html"

# class FilesListView(ListView):
#     model = File
#     context_object_name = 'files_list'
#     template_name = "files/files.html"
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['files_list'] = File.objects \
#             .filter(user=self.request.user) \
#             .order_by("-date")
#         return context
