from shutil import rmtree, copytree, ignore_patterns
import json
import os
import glob


"""
create_almanacs.py

This script will iterate over saved games in ../data/ic
and will copy each game's almanac into ../pelican/content/almanacs

The almanac is named the same as the game file, so for example
    infinite_cleveland_g01_cle15fla14/
becomes
    pelican/content/almanacs/infinite_cleveland_g01_cle15fla14
"""


HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
DATA = os.path.join(ROOT, 'data')
OOTP = os.path.join(DATA, 'ici')
ALMANACS = os.path.join(ROOT, 'pelican', 'content', 'almanacs')


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

    # Copy the almanac to the pelican content almanacs dir
    newsdir = os.path.join(lgdir, 'news')
    src_dir = os.path.join(newsdir, 'almanac_1972')
    dest_dir = os.path.join(ALMANACS, almanac_name)

    if not os.path.exists(src_dir):
        err = f"Error: could not find almanac in dir {src_dir}"
        raise Exception(err)

    if os.path.exists(dest_dir):
        print(f"Found an existing directory at {dest_dir}, removing...")
        rmtree(dest_dir)

    # Find a way to ignore these bloated/unnecessary directories:
    # coaches
    # leagues
    # players
    # teams
    # https://stackoverflow.com/a/42488524
    
    print(f"Copying {src_dir} to {dest_dir}")
    copytree(src_dir, dest_dir, ignore=ignore_patterns('coaches', 'leagues', 'players', 'teams'))

    #break

print("Finished creating almanacs")
