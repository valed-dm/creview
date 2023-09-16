from files.models import File


def save_file(user, path, status):
    file = File(user=user, fpath=path, status=status)
    file.save()
