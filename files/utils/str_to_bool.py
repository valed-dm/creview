def str_to_bool(s):
    if s.lower() in ["true", "false"]:
        return eval(s)
    return s
