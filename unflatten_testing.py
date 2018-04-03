# For json, use a json flattening library (thank goodness this exists!!!!)
from flatten_json import flatten as _flatten
from flatten_json import unflatten_list as _unflatten

# So flatten_json has some issues.
# Particularly, if there is an underscore in the key, it breaks the unflatten.
#
# >>> from flatten_json import flatten
# >>> from flatten_json import unflatten_list as unflatten
# >>> unflatten(flatten({'a_b': 9}))
# {'a': {'b': 9}}
#
# Also, if the key for one of the dictionaries, is a number, that will
# also not unflatten well.
# >>> unflatten(flatten({'a': {'0':7}}))
# {'a': [7]}

# To address these issues, prevent numbers and underscores from being keys.
def _construct_key(previous_key, separator, new_key):
    """
    Returns the new_key if no previous key exists, otherwise concatenates previous key, separator, and new_key
    :param previous_key:
    :param separator:
    :param new_key:
    :return: a string if previous_key exists and simply passes through the new_key otherwise
    """
    # This is changed for ' ' seperator.
    # As such, the separator varible is actually ignored.
    if isinstance(new_key, basestring):
        if new_key == '': #new_key.isdigit() or new_key == '':
            # Append _ to make sure it is not read as a number.
            new_key += "_"
        else:
            new_key = new_key.replace(' ', '_').title()
            
    if previous_key:
        return "{}{}{}".format(previous_key, ' ', new_key)
    else:
        return new_key

def flatten(nested_list_or_dict):
    """Flatten nested dictionaries and lists for easier processing.
       This also allows lists to be flattened."""
    # If iterable, convert to dict.
    if not isinstance(nested_list_or_dict, dict):
        nested_list_or_dict = dict([(str(key), value) for key, value in
                                    enumerate(nested_list_or_dict)])

        # Now, it will be a dict.
        
    # Note, the seperator is redundant as _construct_key overrides it.
    return _flatten(nested_list_or_dict, separator = ' ', _construct_key = _construct_key)

def unflatten(flat_dict):
    """
    Unflatten a dictionary. This may produce either a dictionary, or a list.
    """
    # Actually, nest the dictionary. If the dictionary has numbers as the most
    # outside values, like {'0': 1, '1': 2, '2': 3, '3': 4}, it causes an
    # unexpected error.
    fix_dict = dict([('a ' + key, value) for key, value in flat_dict.items()])

    return _unflatten(fix_dict, separator = ' ')['a']
