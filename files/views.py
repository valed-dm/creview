from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView

from files.forms import UploadFileForm
from files.models import File
from files.utils.get_ext import get_ext
from files.utils.info_upload import info_upload


@csrf_protect
def upload_file(request):
    # handle file upload
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        # Only .py files allowed
        file = request.FILES["file"]
        fname = request.FILES['file'].name
        file_is_py = get_ext(fname) == ".py"
        if form.is_valid() and file_is_py:
            new = File(user=request.user, file=file)
            new.save()
            info_upload(request, fname, file_is_py)
            # Redirect to the file list
            return HttpResponseRedirect("/files/")
        else:
            info_upload(request, fname, file_is_py)
    else:
        # An empty form
        form = UploadFileForm()

    return render(request, "files/upload.html", {"form": form})


class FilesListView(ListView):
    model = File
    context_object_name = 'files_list'
    template_name = "files/files.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files_list'] = File.objects.filter(user=self.request.user)
        return context


class ReportView(ListView):
    template_name = "files/report.html"
