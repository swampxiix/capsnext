import csv, datetime, calendar, os.path

# Constants
CNDIR = '/usr/local/wwrun/capsnext'

def get_csv_rows (fullpath):
    rows = []
    file = open(fullpath, 'rUb')
    r = csv.reader(file, dialect='excel')
    for row in r:
        rows.append(row)
    file.close()
    return rows

def get_next_game (my_sked_file):
#    now_dtd = datetime.date.today()
    # Adjust for EST vs. UTC.
    utc_time = datetime.datetime.now()
    est_time = utc_time + datetime.timedelta(hours=-5)
    now_dtd = est_time.date()
    rows = get_csv_rows(os.path.join(CNDIR, my_sked_file))
    FOUND = None
    x = []
    for game_date, sitch, game_time in rows:
        game_dtd = datetime.datetime.strptime(game_date, '%m/%d/%Y').date()
        if game_dtd >= now_dtd:
            day_of_week = calendar.day_name[game_dtd.weekday()]
            if game_dtd == now_dtd:
                day_of_week = 'TODAY'
            where = 'home'
            if sitch.startswith('at '):
                where = 'away'
                opponent = sitch.replace('at ', '')
            else:
                opponent = sitch
            FOUND = (where, day_of_week, game_date, opponent, game_time)
            break
    return FOUND

import json, urllib2

CAPS_ID = '15'
def get_prev_results():
    all_teams_url = 'https://statsapi.web.nhl.com/api/v1/teams'
    all_teams_dict = json.loads(urllib2.urlopen(all_teams_url).read())
    prev_game_url = 'https://statsapi.web.nhl.com/api/v1/teams/%s?expand=team.schedule.previous' % (CAPS_ID)
    prev_game_dict = json.loads(urllib2.urlopen(prev_game_url).read())
    d = prev_game_dict
    home_id = d['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['home']['team']['id']
    away_id = d['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['away']['team']['id']
    home_abbr, away_abbr = '', ''
    for team in all_teams_dict['teams']:
        if team['id'] == home_id:
            home_abbr = team['abbreviation']
        if team['id'] == away_id:
            away_abbr = team['abbreviation']
    home_scr = d['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['home']['score']
    away_scr = d['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['away']['score']
    FINAL = {
        'home': {'abbr': home_abbr, 'score': home_scr},
        'away': {'abbr': away_abbr, 'score': away_scr},
        }
    return FINAL



