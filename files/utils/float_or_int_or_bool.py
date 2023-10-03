import re

from .str_to_bool import str_to_bool


def float_or_int_or_bool(s):
    m = re.match(r'([+-]?\d+)(?:\.(?:0+|$)|$)', s)
    if m:
        return int(m.group(1))
    else:
        try:
            return float(s)
        except ValueError:
            return str_to_bool(s)
