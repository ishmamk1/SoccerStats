import requests, pandas
from bs4 import BeautifulSoup

# URL to website containing info; requests module to accest website to extrac info.
url = 'https://fbref.com/en/comps/9/Premier-League-Stats'
data = requests.get(url)
bs = BeautifulSoup(data.text, features='html.parser')
leagueTable = bs.select('table.stats_table')[0]

# links - finds the anchor tags with the href of the teams.
links = leagueTable.find_all('a')

# Accesses the teams and filters out unecessary items in hrefList in second line.
hrefList = [i.get('href') for i in links]
hrefList = [i for i in hrefList if '/en/squads/' in i]

clubURLS = [f'https://fbref.com{i}'for i in hrefList]

# Uses input of team to look for it in hrefList. 
# Pandas module used to access table from webpage to print out.
while True:
    ipt = input('Do you want to see standard stats (standard) or matches (match)?: ').lower().strip()
    if ipt == 'standard':
        while True:
            l = input('Club: ').title().split()
            club = '-'.join(l)
            clubINFO = [i for i in clubURLS if club in i]
            if len(clubINFO) > 0:
                info = requests.get(clubINFO[0])
                stats = pandas.read_html(info.text, match='Standard Stats ')
                print(stats)
                break
            else:
                print('Error')
                break

    elif ipt == 'match':
        while True:
            l = input('Club: ').title().split()
            club = '-'.join(l)
            clubINFO = [i for i in clubURLS if club in i]
            if len(clubINFO) > 0:
                pandas.set_option('display.max_columns', None)
                pandas.set_option('display.max_rows', None)
                info = requests.get(clubINFO[0])
                stats = pandas.read_html(info.text, match='Scores & Fixtures')
                print(stats[0])
                break
            else:
                print('Error')
                break
