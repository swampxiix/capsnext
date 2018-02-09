import csv, datetime, calendar, os.path

# Constants
CNDIR = '/usr/local/wwrun/capsnext'
sked_file = 'schedule.csv'

def get_csv_rows (fullpath):
    rows = []
    file = open(fullpath, 'rUb')
    r = csv.reader(file, dialect='excel')
    for row in r:
        rows.append(row)
    file.close()
    return rows

def get_next_game ():
    now_dtd = datetime.date.today()
    rows = get_csv_rows(os.path.join(CNDIR, sked_file))
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

