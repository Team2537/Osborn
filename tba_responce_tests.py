"""
A test script for testing json responce sorting algothms.

"""
try:
    unicode
except NameError:
    unicode = str

try:
    basestring
except NameError:
    basestring = (str, unicode)
    
# Sorting table for annual match types.
match = {
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

# Stats, return
{'ccwms': {'frc1086': 9.163785037028319,
           'frc1111': -37.34717647299759,
           'frc116': -41.168073505614196,
           'frc122': 34.320904506043725,
           'frc1262': 121.9423506914515,
           'frc1418': -2.9382964636358375,
           'frc1522': -18.55524284604979,
           'frc1599': 67.05094468830707,
           'frc1610': -50.392062019711915,
           'frc1629': 118.3153188604076,
           'frc1727': -43.31848024293328,
           'frc1731': 136.29932352094724,
           'frc1885': -22.491766072495334,
           'frc2028': -30.54721938275888,
           'frc2106': -14.064349584732124,
           'frc2199': 23.540051485109785,
           'frc2363': 44.92440060409268,
           'frc2377': -63.61411721574047,
           'frc2534': -40.142392996625624,
           'frc2537': 57.73944917419274,
           'frc2890': 19.111118430180987,
           'frc2914': -63.635188022269126,
           'frc3136': -48.01192895323316,
           'frc3274': -14.438305615514949,
           'frc339': -33.72712417671066,
           'frc346': 30.142341265072623,
           'frc3793': -13.429373188131912,
           'frc384': 84.7562919186943,
           'frc401': 18.01159216855511,
           'frc422': 41.826864547547814,
           'frc4242': -55.23007459267279,
           'frc4456': -34.605988788656276,
           'frc4472': -1.0560818214406122,
           'frc4541': 5.070874407676464,
           'frc5115': -47.20998613644924,
           'frc5243': -47.09359282656331,
           'frc5279': -170.92619166978977,
           'frc5338': -15.860094314778642,
           'frc540': -7.726991501210599,
           'frc5546': 28.695584287093038,
           'frc5587': 11.147523927139774,
           'frc5724': -33.55564861247062,
           'frc5804': 4.111610534537003,
           'frc5945': 23.576598272429933,
           'frc5950': 16.827519044346754,
           'frc5957': -94.94117630196753,
           'frc611': 26.533000699740434,
           'frc612': 79.25231082703897,
           'frc614': 29.877023603107954,
           'frc6194': -29.33649556779083,
           'frc620': -20.018070822656426,
           'frc623': 26.132557363601023,
           'frc6326': -36.124967154426756,
           'frc6334': 84.62839944831234,
           'frc6504': 11.697858326058558,
           'frc6802': -22.79949424699965,
           'frc6882': -81.36679486585678,
           'frc836': 28.827841274545243,
           'frc888': 46.70151468841506,
           'frc977': 5.447792381209118},
 'dprs': {'frc1086': 109.1528472059528,
          'frc1111': 106.69327219925523,
          'frc116': 141.16190251156496,
          'frc122': 87.08394294971433,
          'frc1262': 48.51795161541933,
          'frc1418': 125.27836841721802,
          'frc1522': 133.0718496130705,
          'frc1599': 84.3549603734671,
          'frc1610': 120.82658128125463,
          'frc1629': 61.916445627153905,
          'frc1727': 129.4432844287328,
          'frc1731': 31.805006619020723,
          'frc1885': 127.4737985825407,
          'frc2028': 114.4315458424168,
          'frc2106': 114.89270705048773,
          'frc2199': 102.20824457450077,
          'frc2363': 77.83571280729655,
          'frc2377': 148.3409716112686,
          'frc2534': 134.25196323998497,
          'frc2537': 87.46314767560285,
          'frc2890': 88.95668284379818,
          'frc2914': 114.3797893414244,
          'frc3136': 137.94050367483976,
          'frc3274': 112.70548740810679,
          'frc339': 117.36761017228636,
          'frc346': 90.81029669016122,
          'frc3793': 123.57646085641568,
          'frc384': 90.32745987801127,
          'frc401': 117.66488609679509,
          'frc422': 83.98070243916118,
          'frc4242': 132.37656141999804,
          'frc4456': 107.54527094102207,
          'frc4472': 101.6895225490305,
          'frc4541': 101.7262713815034,
          'frc5115': 115.79916838575011,
          'frc5243': 130.23325025319897,
          'frc5279': 171.01153494307198,
          'frc5338': 98.9496463322416,
          'frc540': 118.02542992999285,
          'frc5546': 108.17135648556075,
          'frc5587': 94.93263534013478,
          'frc5724': 121.70083098407207,
          'frc5804': 117.45452774079826,
          'frc5945': 105.86803694961175,
          'frc5950': 61.87563367074203,
          'frc5957': 163.54556767084858,
          'frc611': 94.485243141187,
          'frc612': 78.59883349938212,
          'frc614': 86.38811819501352,
          'frc6194': 106.89716071580408,
          'frc620': 93.09887683574038,
          'frc623': 108.8673762160621,
          'frc6326': 123.8470179113995,
          'frc6334': 44.26394234075103,
          'frc6504': 112.33008733056977,
          'frc6802': 106.56384511045191,
          'frc6882': 121.64236039209398,
          'frc836': 84.21976254769876,
          'frc888': 86.5619020379734,
          'frc977': 101.74917845470489},
 'oprs': {'frc1086': 118.31663224298093,
          'frc1111': 69.34609572625774,
          'frc116': 99.9938290059506,
          'frc122': 121.40484745575799,
          'frc1262': 170.46030230687091,
          'frc1418': 122.34007195358217,
          'frc1522': 114.5166067670208,
          'frc1599': 151.4059050617743,
          'frc1610': 70.43451926154262,
          'frc1629': 180.23176448756143,
          'frc1727': 86.12480418579958,
          'frc1731': 168.10433013996794,
          'frc1885': 104.98203251004533,
          'frc2028': 83.88432645965787,
          'frc2106': 100.8283574657556,
          'frc2199': 125.74829605961068,
          'frc2363': 122.7601134113891,
          'frc2377': 84.72685439552816,
          'frc2534': 94.1095702433593,
          'frc2537': 145.2025968497955,
          'frc2890': 108.06780127397914,
          'frc2914': 50.744601319155386,
          'frc3136': 89.9285747216066,
          'frc3274': 98.26718179259178,
          'frc339': 83.64048599557552,
          'frc346': 120.95263795523373,
          'frc3793': 110.14708766828366,
          'frc384': 175.08375179670568,
          'frc401': 135.67647826535017,
          'frc422': 125.80756698670893,
          'frc4242': 77.14648682732552,
          'frc4456': 72.93928215236582,
          'frc4472': 100.63344072758987,
          'frc4541': 106.79714578917988,
          'frc5115': 68.58918224930095,
          'frc5243': 83.13965742663567,
          'frc5279': 0.08534327328229097,
          'frc5338': 83.08955201746285,
          'frc540': 110.29843842878228,
          'frc5546': 136.8669407726538,
          'frc5587': 106.0801592672747,
          'frc5724': 88.14518237160131,
          'frc5804': 121.56613827533536,
          'frc5945': 129.44463522204165,
          'frc5950': 78.70315271508858,
          'frc5957': 68.60439136888111,
          'frc611': 121.01824384092744,
          'frc612': 157.85114432642115,
          'frc614': 116.26514179812142,
          'frc6194': 77.56066514801333,
          'frc620': 73.08080601308413,
          'frc623': 134.99993357966326,
          'frc6326': 87.72205075697273,
          'frc6334': 128.89234178906338,
          'frc6504': 124.0279456566283,
          'frc6802': 83.76435086345218,
          'frc6882': 40.275565526237244,
          'frc836': 113.047603822244,
          'frc888': 133.26341672638824,
          'frc977': 107.19697083591392}
}

stats = {'ccwms': {'1086': 9.163785037028319,
           '1111': -37.34717647299759,
           '116': -41.168073505614196,
           '122': 34.320904506043725,
           '1262': 121.9423506914515,
           '1418': -2.9382964636358375,
           '1522': -18.55524284604979,
           '1599': 67.05094468830707,
           '1610': -50.392062019711915,
           '1629': 118.3153188604076,
           '1727': -43.31848024293328,
           '1731': 136.29932352094724,
           '1885': -22.491766072495334,
           '2028': -30.54721938275888,
           '2106': -14.064349584732124,
           '2199': 23.540051485109785,
           '2363': 44.92440060409268,
           '2377': -63.61411721574047,
           '2534': -40.142392996625624,
           '2537': 57.73944917419274,
           '2890': 19.111118430180987,
           '2914': -63.635188022269126,
           '3136': -48.01192895323316,
           '3274': -14.438305615514949,
           '339': -33.72712417671066,
           '346': 30.142341265072623,
           '3793': -13.429373188131912,
           '384': 84.7562919186943,
           '401': 18.01159216855511,
           '422': 41.826864547547814,
           '4242': -55.23007459267279,
           '4456': -34.605988788656276,
           '4472': -1.0560818214406122,
           '4541': 5.070874407676464,
           '5115': -47.20998613644924,
           '5243': -47.09359282656331,
           '5279': -170.92619166978977,
           '5338': -15.860094314778642,
           '540': -7.726991501210599,
           '5546': 28.695584287093038,
           '5587': 11.147523927139774,
           '5724': -33.55564861247062,
           '5804': 4.111610534537003,
           '5945': 23.576598272429933,
           '5950': 16.827519044346754,
           '5957': -94.94117630196753,
           '611': 26.533000699740434,
           '612': 79.25231082703897,
           '614': 29.877023603107954,
           '6194': -29.33649556779083,
           '620': -20.018070822656426,
           '623': 26.132557363601023,
           '6326': -36.124967154426756,
           '6334': 84.62839944831234,
           '6504': 11.697858326058558,
           '6802': -22.79949424699965,
           '6882': -81.36679486585678,
           '836': 28.827841274545243,
           '888': 46.70151468841506,
           '977': 5.447792381209118},
 'dprs': {'1086': 109.1528472059528,
          '1111': 106.69327219925523,
          '116': 141.16190251156496,
          '122': 87.08394294971433,
          '1262': 48.51795161541933,
          '1418': 125.27836841721802,
          '1522': 133.0718496130705,
          '1599': 84.3549603734671,
          '1610': 120.82658128125463,
          '1629': 61.916445627153905,
          '1727': 129.4432844287328,
          '1731': 31.805006619020723,
          '1885': 127.4737985825407,
          '2028': 114.4315458424168,
          '2106': 114.89270705048773,
          '2199': 102.20824457450077,
          '2363': 77.83571280729655,
          '2377': 148.3409716112686,
          '2534': 134.25196323998497,
          '2537': 87.46314767560285,
          '2890': 88.95668284379818,
          '2914': 114.3797893414244,
          '3136': 137.94050367483976,
          '3274': 112.70548740810679,
          '339': 117.36761017228636,
          '346': 90.81029669016122,
          '3793': 123.57646085641568,
          '384': 90.32745987801127,
          '401': 117.66488609679509,
          '422': 83.98070243916118,
          '4242': 132.37656141999804,
          '4456': 107.54527094102207,
          '4472': 101.6895225490305,
          '4541': 101.7262713815034,
          '5115': 115.79916838575011,
          '5243': 130.23325025319897,
          '5279': 171.01153494307198,
          '5338': 98.9496463322416,
          '540': 118.02542992999285,
          '5546': 108.17135648556075,
          '5587': 94.93263534013478,
          '5724': 121.70083098407207,
          '5804': 117.45452774079826,
          '5945': 105.86803694961175,
          '5950': 61.87563367074203,
          '5957': 163.54556767084858,
          '611': 94.485243141187,
          '612': 78.59883349938212,
          '614': 86.38811819501352,
          '6194': 106.89716071580408,
          '620': 93.09887683574038,
          '623': 108.8673762160621,
          '6326': 123.8470179113995,
          '6334': 44.26394234075103,
          '6504': 112.33008733056977,
          '6802': 106.56384511045191,
          '6882': 121.64236039209398,
          '836': 84.21976254769876,
          '888': 86.5619020379734,
          '977': 101.74917845470489},
 'oprs': {'1086': 118.31663224298093,
          '1111': 69.34609572625774,
          '116': 99.9938290059506,
          '122': 121.40484745575799,
          '1262': 170.46030230687091,
          '1418': 122.34007195358217,
          '1522': 114.5166067670208,
          '1599': 151.4059050617743,
          '1610': 70.43451926154262,
          '1629': 180.23176448756143,
          '1727': 86.12480418579958,
          '1731': 168.10433013996794,
          '1885': 104.98203251004533,
          '2028': 83.88432645965787,
          '2106': 100.8283574657556,
          '2199': 125.74829605961068,
          '2363': 122.7601134113891,
          '2377': 84.72685439552816,
          '2534': 94.1095702433593,
          '2537': 145.2025968497955,
          '2890': 108.06780127397914,
          '2914': 50.744601319155386,
          '3136': 89.9285747216066,
          '3274': 98.26718179259178,
          '339': 83.64048599557552,
          '346': 120.95263795523373,
          '3793': 110.14708766828366,
          '384': 175.08375179670568,
          '401': 135.67647826535017,
          '422': 125.80756698670893,
          '4242': 77.14648682732552,
          '4456': 72.93928215236582,
          '4472': 100.63344072758987,
          '4541': 106.79714578917988,
          '5115': 68.58918224930095,
          '5243': 83.13965742663567,
          '5279': 0.08534327328229097,
          '5338': 83.08955201746285,
          '540': 110.29843842878228,
          '5546': 136.8669407726538,
          '5587': 106.0801592672747,
          '5724': 88.14518237160131,
          '5804': 121.56613827533536,
          '5945': 129.44463522204165,
          '5950': 78.70315271508858,
          '5957': 68.60439136888111,
          '611': 121.01824384092744,
          '612': 157.85114432642115,
          '614': 116.26514179812142,
          '6194': 77.56066514801333,
          '620': 73.08080601308413,
          '623': 134.99993357966326,
          '6326': 87.72205075697273,
          '6334': 128.89234178906338,
          '6504': 124.0279456566283,
          '6802': 83.76435086345218,
          '6882': 40.275565526237244,
          '836': 113.047603822244,
          '888': 133.26341672638824,
          '977': 107.19697083591392}
}
# Sorting table for annual match types.
TBA_MATCH_METRICS_DEFAULT_2018 = {
    "actual_time": None, #1520798372,
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

import dpath

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

from pprint import pprint

pprint(flatten(dpath.search(stats, "oprs")))
