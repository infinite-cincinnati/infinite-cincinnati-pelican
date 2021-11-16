import shutil
import re
import os
import glob
import bs4
from bs4 import BeautifulSoup


"""
fix_almanacs.py

This script will iterate over each almanac in ../pelican/content/almanacs
and do various things to clean up almanac pages and remove unused files.
"""


dry_run = False

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
ALMANACS = os.path.join(ROOT, 'pelican', 'content', 'almanacs')


# -----------------------------------------------------------
# function-ify starting here

def unwrap_links(soup):
    """
    unwrap <a> elements (remove links) if link target contains
    removed directories: players/ leagues/ coaches/ teams/

    returns a tuple:
    (soup, n_unwrapped_links)
    """
    unwrapped_links = 0
    hrefs = soup.body.find_all('a')
    for elem in hrefs:
        if (
            'players/' in elem['href']
            or
            'coaches/' in elem['href']
            or 
            'leagues/' in elem['href']
            or
            'teams/' in elem['href']
        ):
            elem.unwrap()
            unwrapped_links += 1
    return (soup, unwrapped_links)


def dissolve_footer(soup):
    """
    Remove the BNN footer, generated date, build, etc.
    This is included with all OOTP pages.
    """
    # Dissolve the BNN footer
    trs = soup.body.table.find_all('tr')
    last_tr = trs[-1]
    last_tr.decompose()

    # Dissolve the generated date and build
    tbls = soup.body.find_all('table')
    last_tbl = tbls[-1]
    last_tbl.decompose()

    return soup


def fix_line_score(soup):
    tbs = soup.body.find_all('table')
    line_score_table = tbs[3]
    line_score_trs = line_score_table.find_all('tr')
    for line_score_tr in line_score_trs:
        line_score_tds = line_score_tr.find_all('td')
        if len(line_score_tds) > 0:
            line_score_td0 = line_score_tds[0]
            team_name = line_score_td0.get_text().strip()
            team_name = re.sub(' 1972', '', team_name)
            line_score_td0.string = team_name

    return soup


def fix_game_notes(soup):
    tbs = soup.body.find_all('table')
    main_table = tbs[0]
    trs = main_table.find_all('tr')
    last_tr = trs[-1]
    td = last_tr.td
    contents = last_tr.td.contents
    attendance_ix = -1
    for i, content in enumerate(contents):
        if content.string is not None:
            if 'EST' in content.string:
                content.string.replace_with("\n6:07 PM Pacific\n")
            if 'Attendance' in content.string:
                attendance_ix = i+1
            if i == attendance_ix:
                content.string.replace_with("\n49,419\n")

    return soup


def fix_game_recap(soup, k):

    # The page layout is managed by one outer table,
    # and the initial line score uses three tables,
    # so index 4 is the table containing the game recap and the WPA
    # index 5 is the table containing the game recap title & text
    tbs = soup.body.find_all('table')
    recap_wpa_table = tbs[5]

    trs = recap_wpa_table.find_all('tr')

    recap_title_elem = trs[0].td

    recap_title_text = recap_title_elem.get_text().strip()
    recap_title_text = re.sub(' 1972', '', recap_title_text)
    recap_title_elem.string = recap_title_text

    # recap_descr_elem = trs[1].td

    # TODO: fix the description...
    # for recap_text in recap_descr_elem.contents:
    #     temp = str(recap_text)
    #     temp = re.sub("Jim Smith", "Jim Leland", temp)
    #     temp = re.sub("Exhibition League", "World Series", temp)
    #     recap_text.string = temp

    # # Modify the game recap text
    # for child in recap_descr_elem.childGenerator():
    #     if type(child)==bs4.element.NavigableString:
    #         if "Jim Smith" in str(child):
    #             import pdb; pdb.set_trace()
    #             text = str(child)
    #             new_text = re.sub("Jim Smith", "Jim Leyland", text)
    #             child.string = new_text
    #         if "Exhibition League" in str(child):
    #             text = str(child)
    #             new_text = re.sub("Exhibition League", "World Series", text)
    #             child.string = new_text

    return soup


def remove_dupe_box_score_header(soup):
    head_tables = soup.find_all("table", class_="head_bg")
    for head_table in head_tables:
        first_tr = head_table.find_all('tr')[0]
        middle_td = first_tr.find_all('td')[1]

        middle_td['style'] = "padding: 75px 0px 0px 0px"

        game_descr_table = middle_td.table
        trs = game_descr_table.find_all('tr')
        trs[0].decompose()
        trs[1].decompose()
        trs[2].decompose()

    return soup


def replace_game_descr_header_box(soup, k, game_log_link=False, box_score_link=False):
    """
    OOTP generated pages have a big header box with a
    game description, but we want to remove it and
    replace it with some game description headers
    of our own.
    """
    # Clear out the contents of the first table row
    tables = soup.body.find_all('table')
    first_table = tables[0]
    trs = first_table.find_all('tr')
    first_tr = trs[0]
    first_tr.decompose()

    # Insert our own header: game 3 world series, teams, and timeline number
    new_tr = soup.new_tag("tr")
    new_td = soup.new_tag("td")

    new_divtitle = soup.new_tag("div")
    new_divtitle['class'] = 'reptitle'
    new_divtitle['class'] += ' text-center'
    new_divtitle.string = "1972 World Series: Game 4"

    new_divsubtitle1 = soup.new_tag("div")
    new_divsubtitle1['class'] = 'repsubtitle'
    new_divsubtitle1['class'] += ' text-center'
    new_divsubtitle1.string = "CINCINNATI REDS @ OAKLAND ATHLETICS"

    new_divsubtitle2 = soup.new_tag("div")
    new_divsubtitle2['class'] = 'repsubtitle'
    new_divsubtitle2['class'] += ' text-center'
    new_divsubtitle2.string = f"OCTOBER 19, 1972"

    new_divsubtitle3 = soup.new_tag("div")
    new_divsubtitle3['class'] = 'repsubtitle'
    new_divsubtitle3['class'] += ' text-center'
    new_divsubtitle3.string = f"TIMELINE {k+1}"

    if game_log_link is True:
        new_divsubtitle4 = soup.new_tag("div")
        new_divsubtitle4['class'] = 'repsubtitle'
        new_divsubtitle4['class'] += ' text-center'
        new_alink = soup.new_tag("a")
        new_alink['href'] = "../game_logs/log_1.html"
        new_alink.string = "GAME LOG"

        new_divsubtitle4.append(new_alink)

    elif box_score_link is True:
        new_divsubtitle4 = soup.new_tag("div")
        new_divsubtitle4['class'] = 'repsubtitle'
        new_divsubtitle4['class'] += ' text-center'
        new_alink = soup.new_tag("a")
        new_alink['href'] = "../box_scores/game_box_1.html"
        new_alink.string = "BOX SCORE"

        new_divsubtitle4.append(new_alink)

    new_td.append(new_divtitle)
    new_td.append(new_divsubtitle1)
    new_td.append(new_divsubtitle2)
    new_td.append(new_divsubtitle3)
    if game_log_link:
        new_td.append(new_divsubtitle4)
    elif box_score_link:
        new_td.append(new_divsubtitle4)

    new_tr.insert(0, new_td)

    soup.body.table.insert(0, new_tr)

    return soup


def fix_head(soup, new_title):
    """
    Fix the <head> element of the soup:
     - dissolve any <link> and <script> elements
     - insert a <meta> tag for charset
     - insert our own <link> elements for css styles
     - fix <title>
     - add infinite cleveland image header
    """
    # Dissolve <link> and <script> elements
    soup.head.link.decompose()

    try:
        soup.head.script.decompose()
    except AttributeError:
        err = "Failed to remove <script> element, "
        err += "it looks like fix_almanacs was already run. "
        err += "Try re-running create_almanacs.py"
        raise Exception(err)

    # Insert a meta charset tag
    new_meta = soup.new_tag("meta", charset="UTF-8")
    soup.head.append(new_meta)

    # Insert our own link elements
    new_links = [
        soup.new_tag("link", rel="stylesheet", type="text/css", href="/theme/css/fonts.css"),
        soup.new_tag("link", rel="stylesheet", type="text/css", href="/theme/css/slate.css"),
        soup.new_tag("link", rel="stylesheet", type="text/css", href="/theme/css/custom.css"),
        soup.new_tag("link", rel="stylesheet", type="text/css", href="/theme/css/ootp.css"),
        soup.new_tag("link", rel="stylesheet", type="text/css", href="/theme/css/infinite.css"),
    ]
    for new_link in new_links:
        soup.head.append(new_link)

    # Insert infinite cleveland header
    new_header = soup.new_tag("header")
    new_header['id'] = "blog-header"
    new_header['class'] = "has-cover"

    new_div = soup.new_tag("div")
    new_div['class'] = "inner"

    new_h1 = soup.new_tag("h1")
    new_h1['class'] = "blog-name cincinnati"

    new_a = soup.new_tag("a", href="/")
    new_a.string = "Infinite Cincinnati"

    new_divcover = soup.new_tag("div")
    new_divcover['class'] = "blog-cover cover"
    new_divcover['style'] = "background-image: url('/img/cin.png');"

    new_h1.append(new_a)
    new_div.append(new_h1)
    new_header.append(new_div)
    new_header.append(new_divcover)
    soup.body.insert(0, new_header)

    soup.title.string = new_title

    return soup


def soupify(filepath):
    """
    Given the path to an HTML file, load it up
    and return it as a BeautifulSoup soup
    """
    with open(filepath, 'r') as f:
        htmldoc = f.read()
    soup = BeautifulSoup(htmldoc, 'html.parser')
    return soup


def filter_box_score_page(almanacdir, k):
    """
    Filter the box score page in the given almanac dir
    """
    print(f"Scrubbing box score file:")

    box_score_file = os.path.join(almanacdir, 'box_scores', 'game_box_1.html')
    print(f" - loading box score file {box_score_file}")
    
    if not os.path.exists(box_score_file):
        err = f"Error: could not find box score file at {box_score_file}"
        raise Exception(err)
    
    soup = soupify(box_score_file)
    
    print(f" - fixing box score head element")
    descr = f"INFCIN{k+1} - Box Score"
    soup = fix_head(soup, descr)
    
    print(f" - fixing (replacing) box score game descr header box")
    soup = replace_game_descr_header_box(soup, k, game_log_link=True)

    # --------------------------
    # unique to this page

    print(f" - removing duplicate header from box score")
    soup = remove_dupe_box_score_header(soup)

    print(f" - fixing line score")
    soup = fix_line_score(soup)

    print(f" - fixing game recap")
    soup = fix_game_recap(soup, k)

    # --------------------------
    
    print(" - dissolving BNN footer")
    soup = dissolve_footer(soup)
    
    print(" - unwrapping links to removed player/league/coach/team dirs")
    (soup, unwrapped_links) = unwrap_links(soup)
    print(f" - unwrapped {unwrapped_links} links")

    # -------------------------
    # also unique, but has to happen after footer removed

    print(f" - fixing game notes")
    soup = fix_game_notes(soup)

    # -------------------------
    
    print(f"Done scrubbing box score file.")
    
    # Now do something with the filtered page
    final_soup = soup.prettify()
    final_soup = re.sub("Jim Smith", "Simyou Lator Engine", final_soup)
    final_soup = re.sub("Exhibition League", "World Series", final_soup)
    if dry_run:
        print('-'*40)
        print(final_soup)
    else:
        with open(box_score_file, 'w') as f:
            f.write(final_soup)


def filter_game_log_page(almanacdir, k):
    """
    Filter game log page
    """
    print(f"Scrubbing game log file:")

    game_log_file = os.path.join(almanacdir, 'game_logs', 'log_1.html')
    print(f" - loading game log file {game_log_file}")

    if not os.path.exists(game_log_file):
        err = f"Error: could not find game log file at {game_log_file}"
        raise Exception(err)

    soup = soupify(game_log_file)

    print(f" - fixing game log head element")
    descr = f"INFCIN{k+1} - PbP Game Log"
    soup = fix_head(soup, descr)

    print(f" - fixing (replacing) game log game descr header box")
    soup = replace_game_descr_header_box(soup, k, box_score_link=True)

    print(" - dissolving BNN footer")
    soup = dissolve_footer(soup)

    print(" - unwrapping links to removed player/league/coach/team dirs")
    (soup, unwrapped_links) = unwrap_links(soup)
    print(f" - unwrapped {unwrapped_links} links")

    # TODO: add a footer link here for more info (OOTP)

    print(f"Done scrubbing game log file.")

    # Now do something with the filtered page
    if dry_run:
        print('-'*40)
        print(soup.prettify())
    else:
        with open(game_log_file, 'w') as f:
            f.write(soup.prettify())


def clean_unused_files(almanacdir):

    def _safe_rm(f):
        try:
            os.remove(f)
        except FileNotFoundError:
            pass

    img_to_rm = glob.glob(
        os.path.join(almanacdir, 'images', '*.png')
    )
    img_to_rm += glob.glob(
        os.path.join(almanacdir, 'images', '*.jpg')
    )
    for img_file in img_to_rm:
        _safe_rm(img_file)

    css_to_rm = glob.glob(
        os.path.join(almanacdir, '*.css')
    )
    for css_file in css_to_rm:
        _safe_rm(css_file)

    person_pics_dir = os.path.join(almanacdir, 'images', 'person_pictures')
    shutil.rmtree(person_pics_dir)


def main():

    almanacdirs = sorted(glob.glob(os.path.join(ALMANACS, '*')))
    for k, almanacdir in enumerate(almanacdirs):
    
        almanac_name = almanacdir.split("/")[-1]
    
        print(f"Filtering almanac {almanac_name}")
    
        # File removal tasks:
        # - remove top level index.html
        index_rm = os.path.join(almanacdir, 'index.html')
        if dry_run is False:
            if os.path.exists(index_rm):
                print(" - removing index.html")
                os.remove(index_rm)
            else:
                err = f"Error: index.html is missing from {almanac_name}, seems like fix_almanacs.py was already run"
                err += "\n(disable this exception if it gets too annoying, it is not required)"
                #raise Exception(err)
                pass

        # BeautifulSoup Tasks:
        # - filter game log page
        # - filter box score page

        # common page tasks:
        # - remove script sorttable.js
        # - replace their css with our own css
        #     - trim down their styles.css
        #     - include our slate/custom after their styles
        #     - include lobster font
        # - modify <table> (which contains... all page contents?)
        #     - removing a <tr> element
        #     - inserting our own custom content (???)
        #     - include a <header> just like on index.html page
        # - dissolve footer
        # - remove all <a> links pointing to removed player/league content

        filter_box_score_page(almanacdir, k)

        filter_game_log_page(almanacdir, k)

        clean_unused_files(almanacdir)


if __name__=="__main__":
    main()
