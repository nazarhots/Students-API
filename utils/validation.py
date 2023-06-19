def validate_empty_values(*args):
    if not all(list(args)):
        return "Values can't be empty", 400