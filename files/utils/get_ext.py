"""Gets a file extension"""

import os


def get_ext(path):
    """Gets a file extension"""

    file, ext = os.path.splitext(path)
    return ext
