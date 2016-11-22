"""Utils module for api views."""


def key_check(model_keys, key):
    """Function the checks if the key is present in the db."""
    if not model_keys:
        return (False, {'error': 'no stock in db'})
    elif key not in model_keys:
        return (False, {'error': 'key not present'})
    return (True, '')
