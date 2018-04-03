"""
Marcus Server

Takes inputs from google sheets.

The input form is cells is

    marcus get matches score breakdown red foulcount

This code in a spreadsheet cell tells the program to load the blue alliance and
call "matches" method on the api.

It then opens the json and gets the
    json()["score"]["breakdown"]["red"]["foulcount"]
for each returned result. These are returned in chronological order (probably
predicted time).


Valid commands:
!Osborn stats oprs
!Osborn stats dprs
!Osborn stats ccwms
!Osborn predictions
!Osborn matches
"""
DEBUG = True

import re
import cmd
import sys
import json
import time
import gspread
import requests
import traceback
from pprint import pprint
from operator import itemgetter
from collections import OrderedDict
from requests.compat import quote_plus as quote
from oauth2client.service_account import ServiceAccountCredentials

from httplib2 import ServerNotFoundError

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
        
try:
    unicode
except NameError:
    unicode = str

try:
    basestring
except NameError:
    basestring = (str, unicode)

try:
    raw_input
except NameError:
    raw_input = input

timeout = 10 # seconds

from math import trunc as _trunc

def truncate(number, digits = 0):
    """Truncate a number to the specified digits.
    Removes the decimal section to be removed, not rounded.
     2.111 ->  2.0
    -2.111 -> -2.0
     1.999 ->  1.0
    -1.999 -> -1.0
    """
    return _trunc(number * 10 ** digits) / 10 ** digits

def get_team_number(team_tag):
    if team_tag.startswith('frc'):
        return int(team_tag[3:])
    else:
        raise ValueError("Not a team tag %r" % team_tag)

class TBAResponceError(BaseException):
    """Base error from connections to the blue alliance."""
    pass

class InvalidEndpointError(TBAResponceError):
    """Invalid Endpoint. Something is wrong with the request."""
    pass

class UnknownTBAError(TBAResponceError):
    """Some other error occured during reading."""
    pass

class NullResponceError(TBAResponceError):
    """The blue alliance returned no data."""
    pass

class BadFormatResponse(TBAResponceError):
    """The blue alliance responded with an unexpected format."""
    pass

class GOsbornError(BaseException):
    """Exeption related to readings from the Osborn script on the sheet."""
    pass

class NoEventError(GOsbornError):
    """No Event to get data for."""
    pass

class BadIndexError(GOsbornError):
    """A index specified is not valid."""
    pass

class Osborn_Command(cmd.Cmd):
    """Simple interface to get data from gsheet."""
    def __init__(self, event):
        self.cache = {}

        self.event = event

        self.tba_auth_key = None

        cmd.Cmd.__init__(self, completekey=None, stdin=None, stdout=None)

    def printcmd(self, cmd):
        """Because everything returns the values, add a printcmd to print out output."""
        pprint(self.onecmd(cmd), stream = self.stdout)

    def get_tba_auth_key(self, file = "client_secret_tba.json"):
        if not self.tba_auth_key:
            with open(file) as f:
                self.tba_auth_key = json.load(f)["tba_auth_key"]
        return self.tba_auth_key

    @staticmethod
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

    @staticmethod
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

    def cache_to(store_key):
        """Decorator to control the caching of urls."""
        # Caches are held between every sheet reading.
        def cachee(func):
            def cache_wrapper(self, *args, **keywords):
                # Get the results so then query from.
                data = self.cache.get(store_key, None)

                if data is None:
                    data = func(self, *args, **keywords)

                    # A none responce means don't overwrite the cache.
                    if not (data is None and store_key in self.cache):
                        self.cache[store_key] = data

                return data

            return cache_wrapper

        return cachee


    def _load_event(self, key):
        """Actually get the data from the blue alliance and return as json."""
        event = self.event
        tba_api = "https://www.thebluealliance.com/api/v3/"
        url = "https://www.thebluealliance.com/api/v3/event/%s/%s?X-TBA-Auth-Key=%s"

        tba_auth_key = self.get_tba_auth_key()

        r = requests.get(url % (quote(event), quote(key), quote(tba_auth_key)),
                         timeout=timeout)

        print(r.url)

        data = r.json()

        # if data is None, then there was no responce.
        if data is None:
            raise NullResponceError()

        # If there is an "error" than there is an error.
        if "errors" in data:
            raise UnknownTBAError(data["errors"])

        return r.json()

    @cache_to('stats')
    def load_stats(self):
        """Load the statistics from the blue alliance."""
        data = self._load_event("oprs")

        # Remove the "frc" from each team though.
        oprs, dprs, ccwms = data['oprs'], data['dprs'], data['ccwms']

        # Remove frc from opr
        oprs = OrderedDict(sorted(
           ((team[3:], opr) for team, opr in oprs.items()),
            key = itemgetter(1, 0), reverse = True))

        # Remove frc from dpr
        dprs = OrderedDict(sorted(
           ((team[3:], dpr) for team, dpr in dprs.items()),
            key = itemgetter(1, 0), reverse = False))

        # Remove frc from ccwm
        ccwms= OrderedDict(sorted(
           ((team[3:],ccwm) for team,ccwm in ccwms.items()),
            key = itemgetter(1, 0), reverse = True))

        data['oprs'], data['dprs'], data['ccwms'] = oprs, dprs, ccwms


        #self.cache['stats'] = data
        return data

    def do_stats(self, value):
        """oprs, dprs, ccwms"""
        value_getter = self._json_link_resolver(value)

        # Get the results so then query from.
        data = self.load_stats()

        value = value_getter(data)

        if isinstance(value, dict):
            value = dict_to_list(flatten(value))

        return value

    @cache_to('matches')
    def load_matches(self):
        """Load the matches from the blue alliance."""
        data = self._load_event("matches")

        # First off, TBA adds an "event key" column.
        # This is completely redundant as there is already match keys and
        # the event key is needed to get the matches anyway.
        # So remove that when we iterate. Also...

        # Remove "frc" from the team names!
        # This includes:
        # [i]['alliances']['blue']['dq_team_keys'][j]
        # [i]['alliances']['blue']['surrogate_team_keys'][j]
        # [i]['alliances']['blue']['team_keys'][j]
        # [i]['alliances']['red']['dq_team_keys'][j]
        # [i]['alliances']['red']['surrogate_team_keys'][j]
        # [i]['alliances']['red']['team_keys'][j]

        # Also, catch a score_breakdown
        # So, if a match has yet to occur, the entire score breakdown is null.
        # This needs to have the keys for score.
        score_breakdown = None
        for match in data:
            # First, make sure that all the fields that SHOULD be present, are!!
##            for metric in TBA_MATCH_FORMAT:
##                if metric not in match:
##                    match[metric] = 
            del match['event_key']
            for alliance in ('red', 'blue'):
                for team_metric in ('team_keys', 'dq_team_keys', 'surrogate_team_keys'):
                    teams = match['alliances'][alliance][team_metric]

                    teams = list(map(get_team_number, teams))

                    # This list also needs exactly 3 elements as there are can be upto
                    # three entiries.
                    while len(teams) < 3: teams.append(None)

                    match['alliances'][alliance][team_metric] = teams

                # Also score defaults to -1 if blank. But it should be None.
                if match['alliances'][alliance]['score'] == -1:
                    match['alliances'][alliance]['score'] = None

            # Print score_breakdown
            if score_breakdown is None:
                score_breakdown = match['score_breakdown']

        # So there is that.
        # Now, if there is a score_breakdown, sanitize it and send it back through.
        if score_breakdown is not None:
            flattened_score = flatten(score_breakdown)

            # Remove all values.
            for key in flattened_score:
                flattened_score[key] = None

            blank_score = unflatten(flattened_score)

            # Brilliant! So now, for any match with score_breakdown == None
            # Replace with blank score.
            for match in data:
                if match['score_breakdown'] is None:
                    match['score_breakdown'] = blank_score
        else:
            # So... There was no score breakdowns of anything.
            # Just leave none for everything. Possibly a future version could
            # save the score_breakdown template and use it for this.
            pass

        # Don't forget, data should be sorted by predicted time.
        data.sort(key=lambda x:(x["actual_time"] or float('inf'),
                                x["predicted_time"] or float('inf'),
                                x["post_result_time"] or float('inf'),
                                x["key"]))

        return data

    def do_matches(self, path):
        """Respond to a request for matches."""
        # Get the results so then query from.
        data = self.cache.get("matches", None)

        # Data is a dictionary, through and through.
        if data is None:
            self.load_matches()
            data = self.cache["matches"]

        path = path.strip()

        if path:
            value_getter = self._json_link_resolver(path)
            value = [value_getter(m) for m in data]
        else:
            value = data

        if value and isinstance(value[0], dict):
            new_value = [dict_to_list(flatten(value[0]))[0]]
            new_value.extend(dict_to_list(flatten(v))[1] for v in value)

            value = new_value

        elif isinstance(value, dict):
            value = dict_to_list(flatten(value))

        # If there was no path, auto rotate table.
        if not path:
            value = list(zip(*value))

        return value

    @cache_to('predictions')
    def load_predictions(self):
        """Load the matches from the blue alliance."""
        try:
            return self._load_event('predictions')
        except NullResponceError:
            print("*** No Predictions from TBA")
            # No responce, don't dump the cache!
            # Unless there is no cache.
            if not 'predictions' in self.cache:
                return {"Error":"No TBA Predictions"}

    def do_predictions(self, value):
        """Respond to a request for matches."""
        value_getter = self._json_link_resolver(value)

        # Get the results so then query from.
        data = self.load_predictions()
        data = self.cache.get('predictions', None)

        # Data is a dictionary, through and through.
        if data is None:
            self.load_predictions()
            data = self.cache['predictions']

        value = value_getter(data)

        if isinstance(value, dict):
            value = dict_to_list(flatten(value))

        return value

    @cache_to('insights')
    def load_insights(self):
        """Load the matches from the blue alliance."""
        return self._load_event('insights')

def update_columns(sheet, row, col, columns, execute = True):
    """Update the specified columns. Row and col are the starting most top left
       cell. Each column should be a list of values. Each list should be the
       same length.
    """
    # Step one, no columns is an error.
    if not columns:
        raise ValueError("Please specify at least one column to update.")

    # Otherwise, get that column length.
    r_len = len(columns[0])
    # First check that all columns are the same length.
    for column in columns[1:]:
        if len(column) != r_len:
            # Variable length.
            raise ValueError("Columns are of varying length.")

    # Start making lists.
    update_cells = []

    # Expand the sheet size if needed.
    if col + len(columns) > sheet.col_count:
        sheet.add_cols(col + len(columns) - sheet.col_count)

    if row + r_len > sheet.row_count:
       sheet.add_rows(row + r_len - sheet.row_count)

    # Get the range of cells to be updated.
    print("Range %s %s %s %s" % (row, col, row + r_len - 1 , col + len(columns) - 1))
    update_range = sheet.range (row, col, row + r_len - 1 , col + len(columns) - 1)

    for c, column in enumerate(columns):

        # Get the range on the sheet for the column.
##        column_range = sheet.range(row, col + c, row + len(column), col + c)
        column_range = (update_range[i] for i in range(c, len(update_range), len(columns)))

        for cell, value in zip(column_range, column):
            # Boolean rational.
            if isinstance(value, bool):
                if str(value).upper() != cell.value:
                    # So its NOT the same.
                    cell.value = value
                    update_cells.append(cell)

            # Use numerical_value for numbers.
            elif isinstance(value, (int, float)):
                # For whatever reason, it looks like gsheets
                # truncates to the 10th place.
                # It seems that 11th & 12th place is almost always correct but
                # can actually differ slightly???
                if cell.numeric_value is None or \
                   truncate(value, 10) != truncate(cell.numeric_value, 10):
                    cell.value = value
                    update_cells.append(cell)

            # And for everything else, string handling.
            elif isinstance(value, basestring):
                if value != cell.value:
                    cell.value = value
                    update_cells.append(cell)

            # Handle None
            elif value is None:
                if '' != cell.value:
                    # Set to ''
                    cell.value = ''
                    update_cells.append(cell)

            else:
                # Other type, error.
                raise ValueError("Cell value %r must be of type string, number, "
                                 "or boolean. Not %s." % (value, type(value)))

    # Now take the list of cells and call an update.
    if execute:
        print("Updating %d cells." % len(update_cells))
        if update_cells:
            sheet.update_cells(update_cells)
        return len(update_cells)
    else:
        return update_cells

##def flatten_dict(d):
##    """Flatten a dictionary down."""
##    def expand(key, value):
##        if isinstance(value, dict):
##            return [ (key.replace('_', '__') + '_' + k, v) for k, v in flatten_dict(value).items() ]
##        else:
##            return [ (key, value) ]
##
##    items = [ item for k, v in d.items() for item in expand(k, v) ]
##
##    return dict(items)
##
##from collections import Iterable
##
###https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
##def flatten_list(items):
##    """Yield items from any nested iterable; see REF."""
##    for x in items:
##        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
##            yield from flatten(x)
##        else:
##            yield x

def dict_to_list(d):
    return list(zip(*d.items()))

##def flatten(items):
##    """Flattens a list, dictionary, or set into lists nested two deep at most.
##       Ignores strings and bytes.
##    """
##    # If this is a dictionary, process that.
##    if isinstance(items, dict): # Ordereddicts also are counted here
##        value = list(zip(*flatten_dict(items).items()))
##
##        return value
##
##    elif isinstance(items, Iterable) and not isinstance(items, (str, bytes)):
##        value = list(flatten_list(items))
##
##        return value
##
##    else:
##        return items

def main(url):
    global client, sheet, value, command_cells, command_reader
    # Sign into google sheets.
    start = time.time()
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret_gsheet.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(url).sheet1

    stop = time.time()
    print("Signed into Sheet in %.3f seconds." % (stop - start))

    # Find all command cells
    start = time.time()
    command_cells = sheet.findall(re.compile("^!Osborn", re.I))
    stop = time.time()
    print("Found %d command cells in %.3f seconds." % (len(command_cells), stop - start))

    # Find the "!Osborn event" first.
    start = time.time()
    event = None
    for c in command_cells:
        if str(c.value).lower().startswith("!osborn event"):
            event = str(c.value)[14:]
            break

    if event is None:
        raise NoEventError()
    stop = time.time()
    print("Found the event command in %.3f seconds" % (stop - start))

    # Build the analyizer and get the data.

    # Build the reader with the event.
    start = time.time()
    command_reader = Osborn_Command(event)

    signals = []
    # So for the remaining commands run it!
    for command in command_cells:
        if command == c:
            continue
        try:
            value = command_reader.onecmd(command.value[8:])
        except NullResponceError:
            print("Null Responce from TBA %s" % command.value)

        except ServerNotFoundError:
            print("Could not connect to google.")

        except requests.exceptions.ConnectTimeout:
            # Connection Timed out.
            # 10 seconds probably.
            print("Connection timed out.")

        else:
            if value:
                signals.append((command.row + 1, command.col, value))

    stop = time.time()
    print("Analyzied statistics in %.3f seconds." % (stop - start))
    start = time.time()

    # Update spread sheet.
    for row, col, value in signals:
        update_columns(sheet, row, col, value)

    stop = time.time()
    print("Updated Sheet in %.3f seconds." % (stop - start))

if __name__ == '__main__':
    if sys.argv[1:]:
        url = sys.argv[1]
    else:
        url = raw_input("URL: ").strip()
    # Sign into google sheets.
    t = 60
    while True:
        try:
            main(url)

            print("Waiting", end = '', flush = True)
            time.sleep(t/4)
            print(".", end = '', flush = True)
            time.sleep(t/4)
            print(".", end = '', flush = True)
            time.sleep(t/4)
            print(".", end = '', flush = True)
            time.sleep(t/4)
            print("") # The newline.

        except KeyboardInterrupt:
            # Reraise that execptions. Prevent this from
            # going into the general error case.
            raise
        
        except ServerNotFoundError:
            print("Server not found.")
            time.sleep(.5) # Wait for things to change.

        except NoEventError:
            print("No event found on sheet.")
            time.sleep(.5) # Wait for things to change.

        except BadIndexError:
            print("Bad index %s" % list(sys.exc_info()[1].args))
            time.sleep(.5) # Wait for things to change.

        except gspread.exceptions.RequestError:
            # Connection Error.
            # Probably caused by dodgy internet on this end. Though it is
            # impossible to tell. This is a general error.
            print("gspread.exceptions.RequestError, %s" % list(sys.exc_info()[1].args))

        except:
            # If there is some odd error, keep executing.
            # This battle station must stay online!!!
            traceback.print_exc()

            # If we are in debug mode, auto start debugging.
            if DEBUG:
                import pdb
                pdb.post_mortem(sys.exc_info()[2])
                break
            else:
                # Continue execution, however, because internet problems
                # is possible cause, wait a little to wait for things to change.
                time.sleep(.5)
