from distutils.dir_util import copy_tree
import json
import os
import glob


"""
fix_wpa_figs.py

This script will look for WPA figures inside the save file,
and if necessary, copy them from news/html/ to news/almanac/
"""


dry_run = False

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
DATA = os.path.join(ROOT, 'data')
OOTP = os.path.join(DATA, 'ici')


if not os.path.exists(OOTP):
    raise Exception(f"Could not find OOTP save files at {OOTP}")

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

    almanac_name = gamedir.split("/")[-1]

    # Now we can traverse the known directory structure
    # of a saved OOTP game.
    newsdir = os.path.join(lgdir, 'news')

    almanacdir = os.path.join(newsdir, 'almanac_1972')
    almanacimgdir = os.path.join(almanacdir, 'images')
    almanacwpadir = os.path.join(almanacdir, 'images', 'wpa')

    htmlwpadir = os.path.join(newsdir, 'html', 'images', 'wpa')

    # By default, the almanac_1972/images/wpa directory does not exist
    if not os.path.exists(almanacwpadir):

        # If it does not exist, copy html/images/wpa to almanac_1972/images/wpa
        print(f"Did not find WPA directory in {almanac_name} almanac, fixing WPA images")
        if os.path.exists(htmlwpadir):
            if dry_run:
                print(f"[simulating] cp -r {htmlwpadir} {almanacwpadir}")
            else:
                copy_tree(htmlwpadir, almanacwpadir)
        else:
            err = f"Error: Could not find WPA images in html/images/wpa for almanac {almanac_name}:\n"
            err += f"{htmlwpadir}"
            raise Exception(err)
    else:
        print(f"Found an existing WPA directory in {almanac_name} almanac, no need to fix")

print("Finished fixing WPA images")
