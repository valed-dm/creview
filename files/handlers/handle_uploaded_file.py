"""Handles csv file uploading"""
import csv
import io
import os

from files.models import File
from files.utils.convert_size import convert_bytes
from files.utils.get_ext import get_ext
from files.utils.info_upload import info_upload


def handle_uploaded_file(request):
    """Uploads new or review existing csv file"""

    user = request.user
    file = request.FILES["file"]
    fname = file.name
    fsize = convert_bytes(file.size)
    is_csv = get_ext(fname) == ".csv"
    info_upload(request, fname, is_csv)

    if is_csv:
        f = file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(f))
        fieldnames = ", ".join(reader.fieldnames)
        status = "new"

        # searches db among user's files for a match
        prev_file = File.objects \
            .filter(file_name=fname).all() \
            .filter(user=user).first()
        if prev_file:
            status = "reviewed"
            prev_file_path = prev_file.file.path
            os.remove(prev_file_path)
            prev_file.delete()

        file = File(
            file=file,
            file_name=fname,
            size=fsize,
            headers=fieldnames,
            user=user,
            status=status
        )
        file.save()

        return True
    else:
        return False
