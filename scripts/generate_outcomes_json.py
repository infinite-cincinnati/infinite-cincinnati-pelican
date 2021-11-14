import json
import os
import glob

"""
generate_outcomes_json.py

This script uses data in ../data/ici
to generate outcomes data in ../data/outcomes.json

outcomes.json data structure:
    [
        {
            "WName": "Cincinnati",
            "WBkgColor": "d51313",
            "WTxtColor": "#eeeeee",
            "WRuns": 7,
            "LName": "Florida",
            "LBkgColor": "00843d",
            "LTxtColor": "ffcd00",
            "LRuns": 6,
            "Innings": 9,
            "AlmanacName": "infinite_cincinnati_g01_XYZ"
        }
    ]
"""


CIN_BKG_COLOR = "d51313"
CIN_TXT_COLOR = "eeeeee"
OAK_BKG_COLOR = "00843d" # green
OAK_TXT_COLOR = "ffcd00" # yellow

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
DATA = os.path.join(ROOT, 'data')
OOTP = os.path.join(DATA, 'ici')


outcomes_json = []
gamedirs = sorted(glob.glob(os.path.join(OOTP, '*')))
for k, gamedir in enumerate(gamedirs):
    gamefiles = glob.glob(os.path.join(gamedir, '*'))
    lgdir = None
    for gamefile in gamefiles:
        if gamefile[-3:] == '.lg':
            lgdir = gamefile
    if lgdir is None:
        raise Exception(f"Could not find .lg file for {gamedir}")

    # Now we can traverse the known directory structure
    # of a saved OOTP game.

    # We are only interested in games.csv
    csvdir = os.path.join(lgdir, 'import_export', 'csv')
    gamescsv = os.path.join(csvdir, 'games.csv')

    # Structure:
    # game_id,league_id,home_team,away_team,attendance,date,time,game_type,played,dh,innings,runs0,runs1,hits0,hits1,errors0,errors1,winning_pitcher,losing_pitcher,save_pitcher,starter0,starter1
    # 1,100,2,1,30878,"1997-10-1",2005,3,1,0,9,11,7,14,15,0,2,9,27,0,17,41
    with open(gamescsv, 'r') as f:
        gamescsvlines = f.readlines()
    data = gamescsvlines[1].split(",")
    innings = int(data[10])
    cin_runs = int(data[11])
    oak_runs = int(data[12])
    if oak_runs > cin_runs:
        wname = "Oakland"
        wtxtcolor = OAK_TXT_COLOR
        wbkgcolor = OAK_BKG_COLOR
        wruns = oak_runs
        lname = "Cincinnati"
        ltxtcolor = CIN_TXT_COLOR
        lbkgcolor = CIN_BKG_COLOR
        lruns = cin_runs
    else:
        lname = "Oakland"
        ltxtcolor = OAK_TXT_COLOR
        lbkgcolor = OAK_BKG_COLOR
        lruns = oak_runs
        wname = "Cincinnati"
        wtxtcolor = CIN_TXT_COLOR
        wbkgcolor = CIN_BKG_COLOR
        wruns = cin_runs

    almanac_name = gamedir.split("/")[-1]

    dat = {
        "Index": k,
        "WName": wname,
        "WBkgColor": wbkgcolor,
        "WTxtColor": wtxtcolor,
        "WRuns": wruns,
        "LName": lname,
        "LBkgColor": lbkgcolor,
        "LTxtColor": ltxtcolor,
        "LRuns": lruns,
        "Innings": innings,
        "AlmanacName": almanac_name
    }
    outcomes_json.append(dat)

outcomes_json_file = os.path.join(DATA, 'outcomes.json')
with open(outcomes_json_file, 'w') as f:
    json.dump(outcomes_json, f, indent=4)

print(f"Finished generating outcomes in {outcomes_json_file}")
