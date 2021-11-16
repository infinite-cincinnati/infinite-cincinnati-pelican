import shutil
import json
import os
import glob


"""
extract_data.py

This script extracts CSV data from OOTP save files,
and processes the data to make it more convenient.

CSV files to save:

games.csv
games_score.csv
players.csv
players_game_batting.csv
players_game_pitching_stats.csv
players_at_bat_batting_stats.csv
teams.csv
"""


HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
DATA = os.path.join(ROOT, 'data')
OOTP = os.path.join(DATA, 'ic')


def write_csv_lines(csvdat, csvdir, csvname):
    """
    Given a chunk of data, a directory, and a filename,
    write the contents of csvdat to csvdir/csvname
    """
    csvfile = os.path.join(csvdir, csvname)
    csvdat = [j.strip() for j in csvdat]
    with open(csvfile, 'w') as f:
        f.write("\n".join(csvdat))


def fetch_csv_lines(csvdir, csvname):
    """
    Given a directory and a filename,
    fetch the contents of csvdir/csvname
    and return it as a list of stripped strings.
    """
    csvfile = os.path.join(csvdir, csvname)
    if not os.path.exists(csvfile):
        err = f"Error: could not find {csvname} in {csvdir}"
        raise FileNotFoundError(err)
    with open(csvfile, 'r') as f:
        csvlines = f.readlines()
    csvlines = [j.strip() for j in csvlines]
    return csvlines


def insert_timeline_csv_data(csvdata, timeline):
    """
    Given a list of strings (CSV data),
    insert the timeline value at the
    front of each line (first column).
    """
    new_csvdata = []
    for line in csvdata:
        new_csvdata.append(f"{timeline},{line}")
    return new_csvdata


def copy_csv_data(csvdir, destdir, csvname, timeline=-1):
    """
    Given the name of a csv file X.csv,
    load up data from X.csv in csvdir,
    append a timeline column to the front of each line,
    and dump it to X.csv in destdir.
    """
    csvlines = fetch_csv_lines(csvdir, csvname)
    csvdata = csvlines[1:]
    if timeline >= 0:
        timeline_csvdata = insert_timeline_csv_data(csvdata, timeline)
    else:
        timeline_csvdata = csvdata

    destlines = fetch_csv_lines(destdir, csvname)
    destlines += timeline_csvdata
    write_csv_lines(destlines, destdir, csvname)


def init(csvdir, destdir, csvname, timeline=True):
    """
    Given the name of a csv file X.csv,
    Look for X.csv in csvdir.
    If found, copy the header to X.csv in destdir
    (add a 'timeline' column to the very front).
    If not found, die.
    """
    csvlines = fetch_csv_lines(csvdir, csvname)
    head = csvlines[0].strip()
    if timeline:
        head = "timeline," + head

    destfile = os.path.join(destdir, csvname)
    if os.path.exists(destfile):
        os.remove(destfile)
    with open(destfile, 'w') as f:
        f.write(head)


def main():

    destdir = os.path.join(DATA, 'csv')
    try:
        os.mkdir(destdir)
    except FileExistsError:
        shutil.rmtree(destdir)
        os.mkdir(destdir)

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
    
        csvdir = os.path.join(lgdir, 'import_export', 'csv')

        # No timeline specified, these don't change timeline to timeline
        if k==0:
            print("Copying teams and players to new CSV data")
            init(csvdir, destdir, 'players.csv', timeline=False)
            init(csvdir, destdir, 'teams.csv', timeline=False)

            # Only copy once
            copy_csv_data(csvdir, destdir, 'players.csv')
            copy_csv_data(csvdir, destdir, 'teams.csv')

        # Initialize headers once
        if k==0:
            print("Initializing headers for new CSV data")
            init(csvdir, destdir, 'games.csv')
            init(csvdir, destdir, 'games_score.csv')
            init(csvdir, destdir, 'players_game_batting.csv')
            init(csvdir, destdir, 'players_game_pitching_stats.csv')
            init(csvdir, destdir, 'players_at_bat_batting_stats.csv')

        print(f"Copying timeline {k+1} data to new CSV data")
        copy_csv_data(csvdir, destdir, 'games.csv', k)
        copy_csv_data(csvdir, destdir, 'games_score.csv', k)
        copy_csv_data(csvdir, destdir, 'players_game_batting.csv', k)
        copy_csv_data(csvdir, destdir, 'players_game_pitching_stats.csv', k)
        copy_csv_data(csvdir, destdir, 'players_at_bat_batting_stats.csv', k)


if __name__=="__main__":
    main()
