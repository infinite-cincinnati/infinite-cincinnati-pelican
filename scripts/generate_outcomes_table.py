import json
import os


"""
generate_outcomes_table.py

This script uses data in ../data/outcomes.json
to generate a table of outcomes in ../pelican/content/index.html
"""


dry_run = False

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
DATA = os.path.join(ROOT, 'data')
PELICANCONTENT = os.path.join(ROOT, 'pelican', 'content')


index_html_file = os.path.join(PELICANCONTENT, 'index.html')
print(f"Loading existing index.html file from {index_html_file}")
with open(index_html_file, 'r') as f:
    index_html = f.readlines()

# Preserve content before/after table
new_index_html_top = []
for line in index_html:
    if "BEGIN INFINITE CINCINNATI TABLE" in line:
        new_index_html_top.append(line)
        break
    else:
        new_index_html_top.append(line)

new_index_html_bot = []
reached = False
for line in index_html:
    if "END INFINITE CINCINNATI TABLE" in line:
        reached = True
        new_index_html_bot.append(line)
    elif reached:
        new_index_html_bot.append(line)

# Assemble the actual table
table_head = """
        <table class="table" style="text-align: center; border: 1px solid black;">
            <thead>
                <tr>
                    <th width="150">Game</th>
                    <th>Winnner</th>
                    <th width="150">Score</th>
                    <th>Loser</th>
                    <th width="150">Innings</th>
                    <th width="300">Links</th>
                </tr>
            </thead>
            <tbody>
"""

table_tail = """
            </tbody>
        </table>
"""

table_row_template = """
                <tr>
                    <td>
                        Timeline {game_index}
                    </td>
                    <td style="background-color: #{winner_bkg_color}; color: #{winner_txt_color}; font-weight: bold;">{winner_name}</td>
                    <td>{winner_runs}-{loser_runs}</td>
                    <td style="background-color: #{loser_bkg_color}; color: #{loser_txt_color};">{loser_name}</td>
                    <td>({innings})</td>
                    <td>
                        <a style="text-decoration: none;" href="almanacs/{almanac_name}/box_scores/game_box_1.html">
                        <button class="btn btn-small btn-secondary">Box Score</button>
                        </a>
                        <a style="text-decoration: none;" href="almanacs/{almanac_name}/game_logs/log_1.html">
                        <button class="btn btn-small btn-secondary">Play By Play</button>
                        </a>
                    </td>
                </tr>
"""

outcomes_json_file = os.path.join(DATA, 'outcomes.json')
if not os.path.exists(outcomes_json_file):
    raise Exception(f"Error: could not find outcomes.json file {outcomes_json_file}")
with open(outcomes_json_file, 'r') as f:
    outcomes_json = json.load(f)

new_index_html_table = []

eras = [
    "1972 Strategy Engine",
    "1942 Strategy Engine",
    "1982 Strategy Engine",
    "1997 Strategy Engine",
    "2017 Strategy Engine",
]
for i, outcome in enumerate(outcomes_json):
    if i%11==0:
        title_txt = f'<h2>{eras[i//11]}</h2>'
        new_index_html_table.append(title_txt)
        new_index_html_table.append(table_head)

    table_row = table_row_template.format(
        game_index=outcome['Index']+1,
        winner_name=outcome['WName'],
        winner_bkg_color=outcome['WBkgColor'],
        winner_txt_color=outcome['WTxtColor'],
        winner_runs=outcome['WRuns'],
        loser_name=outcome['LName'],
        loser_bkg_color=outcome['LBkgColor'],
        loser_txt_color=outcome['LTxtColor'],
        loser_runs=outcome['LRuns'],
        innings=outcome['Innings'],
        almanac_name=outcome['AlmanacName']
    )
    new_index_html_table.append(table_row)

    if i%11==10:
        new_index_html_table.append(table_tail)

# Assemble the final index.html file
page_text = ""
page_text += "".join(new_index_html_top)
page_text += "\n".join(new_index_html_table)
page_text += "".join(new_index_html_bot)

if dry_run:
    print('-----------------------------------')
    print(page_text)
else:
    print(f"Writing new index.html file to {index_html_file}")
    with open(index_html_file, 'w') as f:
        f.write(page_text)

