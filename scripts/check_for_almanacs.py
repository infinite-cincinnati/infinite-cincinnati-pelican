import os
import glob
from bs4 import BeautifulSoup


"""
fix_almanacs.py

This script will iterate over each almanac in ../pelican/content/almanacs
and do various things to clean up almanac pages and remove unused files.
"""


dry_run = True

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
DATA = os.path.join(ROOT, 'data')
OOTP = os.path.join(DATA, 'ici')


if not os.path.exists(OOTP):
    raise Exception(f"Could not find OOTP save files at {OOTP}")

gamedirs = sorted(glob.glob(os.path.join(OOTP, '*')))
for k, gamedir in enumerate(gamedirs):

    gamefiles = glob.glob(os.path.join(gamedir, '*'))
    lgdir = None
    for gamefile in gamefiles:
        if gamefile[-3:] == '.lg':
            lgdir = gamefile
    if lgdir is None:
        raise Exception(f"Could not find .lg file for {gamedir}")

    almanac_name = gamedir.split("/")[-1]

    # Copy the almanac to the pelican content almanacs dir
    newsdir = os.path.join(lgdir, 'news')
    if not os.path.exists(newsdir):
        err = f"Error: could not find news directory for {almanac_name}: no directory {newsdir}"
        raise Exception(err)

    almanacdir = os.path.join(newsdir, 'almanac_1972')
    if not os.path.exists(almanacdir):
        err = f"Error: could not find almanac directory for {almanac_name}: no directory {almanacdir}"
        raise Exception(err)

    logsdir = os.path.join(almanacdir, 'game_logs')
    if not os.path.exists(logsdir):
        err = f"Error: could not find almanac data for {almanac_name}: no game_logs directory {logsdir}"
        raise Exception(err)
