
def resolve_osborn_word_maker(word):
    """Take the osborn word and give a function to apply to the list."""
    # First, of the world is a integer, use it to get an element from list.
    if word.isdigit():
        return itemgetter(int(word))

##        # If it is "*", handle it as a list wild card. Apply following critera
##        # to all elements in list and return this list.
##        elif word == "*":
##            def a(data):
##

    # Otherwise, use this as a key for a dictionary.
    else:
        return itemgetter(word)


def _json_link_resolver(link, sort_key = None):
    """Take the json and build the list of links from that.
    json should either be a nested dictionary, or a list of dictionaries.

    Returns a function that will get the needed values from json.
    """
    itemgetters = map(itemgetter, link.split())

    def get_link(json):
        try:
            for getter in itemgetters:
                json = getter(json)
            return json
        except KeyError:
            raise BadIndexError(sys.exc_info()[1].args)
        except IndexError:
            raise BadIndexError(sys.exc_info()[1].args)
##            except TypeError:
##                # This is from (1,2,3)["test"]
##                raise BadIndexError(sys.exc_info()[1].args)

    return get_link
