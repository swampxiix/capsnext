from WebKit.Page import Page
from z_cn_tools import get_next_game, CNDIR

import os.path
my_sked_file = os.path.join(CNDIR, 'schedule.csv')

class Index (Page):
    def title (self):
        return 'The Next Caps Game is...'

    def writeHeadParts(self):
        self.writeln('<link href="https://fonts.googleapis.com/css?family=Oswald" rel="stylesheet">')
        self.writeln('<link href="capsnext.css" rel="stylesheet">')

    def writeContent(self):
        wr = self.writeln
        try:
            where, day_of_week, game_date, opponent, game_time = get_next_game(my_sked_file)
            wr('<div id="content">')
            h1class = 'future'
            if day_of_week == 'TODAY':
                h1class = 'today'

            wr('<h1 class="%s"><img src="capslogo.png"> NEXT GAME</h1>' % (h1class))
            wr('<h3>%s<br>' % (day_of_week))
            wr('%s<br>%s PM</h3>' % (game_date, game_time))
            wr('<h2>%s<br>' % (where.upper()))
            imgname = opponent.replace('.', '')
            imgname = imgname.replace(' ', '')
            imgname = imgname.lower()
            wr('<img src="logos_hockey/%s.gif"><br>' % (imgname))
            wr('%s</h2>' % (opponent))
            wr('</div>')
        except TypeError:
            wr('No upcoming games.')