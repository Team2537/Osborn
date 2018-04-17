import fnmatch
x = {
    "actual_time": 1520798372,
    "alliances": {
      "blue": {
        "dq_team_keys": [],
        "score": 343,
        "surrogate_team_keys": [],
        "team_keys": [
          "frc1885",
          "frc1731",
          "frc4456"
        ]
      },
      "red": {
        "dq_team_keys": [],
        "score": 248,
        "surrogate_team_keys": [],
        "team_keys": [
          "frc1629",
          "frc225",
          "frc3793"
        ]
      }
    },
    "comp_level": "f",
    "event_key": "2018vagdc",
    "key": "2018vagdc_f1m1",
    "match_number": 1,
    "post_result_time": 1520798539,
    "predicted_time": 1520798403,
    "score_breakdown": {
      "blue": {
        "adjustPoints": 0,
        "autoOwnershipPoints": 12,
        "autoPoints": 27,
        "autoQuestRankingPoint": False,
        "autoRobot1": "AutoRun",
        "autoRobot2": "AutoRun",
        "autoRobot3": "AutoRun",
        "autoRunPoints": 15,
        "autoScaleOwnershipSec": 6,
        "autoSwitchAtZero": False,
        "autoSwitchOwnershipSec": 0,
        "endgamePoints": 65,
        "endgameRobot1": "Climbing",
        "endgameRobot2": "Levitate",
        "endgameRobot3": "Parking",
        "faceTheBossRankingPoint": False,
        "foulCount": 0,
        "foulPoints": 10,
        "rp": 0,
        "tba_gameData": "LLL",
        "techFoulCount": 1,
        "teleopOwnershipPoints": 196,
        "teleopPoints": 306,
        "teleopScaleBoostSec": 0,
        "teleopScaleForceSec": 10,
        "teleopScaleOwnershipSec": 59,
        "teleopSwitchBoostSec": 10,
        "teleopSwitchForceSec": 0,
        "teleopSwitchOwnershipSec": 127,
        "totalPoints": 343,
        "vaultBoostPlayed": 1,
        "vaultBoostTotal": 3,
        "vaultForcePlayed": 2,
        "vaultForceTotal": 3,
        "vaultLevitatePlayed": 3,
        "vaultLevitateTotal": 3,
        "vaultPoints": 45
      },
      "red": {
        "adjustPoints": 0,
        "autoOwnershipPoints": 8,
        "autoPoints": 23,
        "autoQuestRankingPoint": False,
        "autoRobot1": "AutoRun",
        "autoRobot2": "AutoRun",
        "autoRobot3": "AutoRun",
        "autoRunPoints": 15,
        "autoScaleOwnershipSec": 4,
        "autoSwitchAtZero": False,
        "autoSwitchOwnershipSec": 0,
        "endgamePoints": 65,
        "endgameRobot1": "Climbing",
        "endgameRobot2": "Parking",
        "endgameRobot3": "Levitate",
        "faceTheBossRankingPoint": False,
        "foulCount": 2,
        "foulPoints": 25,
        "rp": 0,
        "tba_gameData": "LLL",
        "techFoulCount": 0,
        "teleopOwnershipPoints": 90,
        "teleopPoints": 200,
        "teleopScaleBoostSec": 10,
        "teleopScaleForceSec": 0,
        "teleopScaleOwnershipSec": 69,
        "teleopSwitchBoostSec": 0,
        "teleopSwitchForceSec": 10,
        "teleopSwitchOwnershipSec": 11,
        "totalPoints": 248,
        "vaultBoostPlayed": 3,
        "vaultBoostTotal": 3,
        "vaultForcePlayed": 1,
        "vaultForceTotal": 3,
        "vaultLevitatePlayed": 3,
        "vaultLevitateTotal": 3,
        "vaultPoints": 45
      }
    },
    "set_number": 1,
    "time": 1520800200,
    "videos": [
      {
        "key": "bdJEq5ZnT00",
        "type": "youtube"
      },
      {
        "key": "vmmf2uZBuLc",
        "type": "youtube"
      }
    ],
    "winning_alliance": "blue"
  }

def match(s, pat):
    try:
        return fnmatch.fnmatch(s, pat)
    except TypeError:
        return False

def select(ds, pat):
    return [d[k] for d in ds for k in d if match(k, pat)]

def set(ds, k, v):
    for d in ds:
        d[k] = v

# Test the flatten/unflatten function.
from pprint import pprint
from flatten_json import flatten, unflatten_list as unflatten

pprint(x)

flat = flatten(x)

##pprint(flat)

unflat = unflatten_list(flat)

pprint(unflat)

if x == unflat:
    print("Success!")
else:
    print("Failure")
