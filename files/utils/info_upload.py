from django.contrib import messages


def info_upload(request, file_name, file_is_py):
    if file_is_py:
        messages.info(
            request,
            f"'{file_name}' was successfully uploaded to "
            f"{request.user.email}\'s list."
        )
    else:
        messages.info(
            request,
            f"Upload failed. '{file_name}' doesn't end with '.py'"
        )
