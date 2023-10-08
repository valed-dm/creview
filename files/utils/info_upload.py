"""Informs on file upload success"""
from django.contrib import messages


def info_upload(request, file_name, is_csv):
    """Emits upload's messages"""

    if is_csv:
        messages.info(
            request,
            f"'{file_name}' is uploaded to "
            f"{request.user.email}\'s list."
        )
    else:
        messages.info(
            request,
            f"Upload failed for '{file_name}'"
        )
