import httpx
import sys
from bs4 import BeautifulSoup
import sqlite3

class State:
  def __init__(self, name, cities, link):
    self.name = name
    self.cities = cities
    self.link = link

class City:
  def __init__(self, name, link, shows):
    self.name = name
    self.link = link
    self.shows = shows

class Show:
  def __init__(self, name, time, date,  venue, address, freq, cost, email, link, phone, hostname):
    self.name = name
    self.link = link
    self.time = time
    self.date = date
    self.venue = venue
    self.address = address
    self.freq = freq
    self.cost = cost
    self.email = email
    self.phone = phone
    self.hostname = hostname

main_page = httpx.get('https://badslava.com/')
soup = BeautifulSoup(main_page.text, 'html.parser')
united_states_geoblock = (soup.find('div', class_='united-states'))

state_geounits = list(united_states_geoblock.find_all('div', class_='geoUnit'))

all_states_data = []

for i in range(0,len(state_geounits)):
    curr_cities = [] 
    curr_state_soup = state_geounits[i]
    state_name = curr_state_soup.find('h3').find('a').text
    state_link = curr_state_soup.find('h3').find('a').get('href')
    
    soup_cities = list(curr_state_soup.find_all('li'))
    for soup_city in soup_cities:
        curr_city_req = httpx.get("https://badslava.com/" + soup_city.find('a').get('href'))
        curr_city_soup= BeautifulSoup(curr_city_req.text, 'html.parser')
        curr_cities_shows = []

        div_table_soup = curr_city_soup.find('div', class_='table-responsive')

        dates =  div_table_soup.find_all('font', {'color': 'red'})
        show_tables =  div_table_soup.find_all('table', {'class': 'table'})
        if(len(dates)!=len(show_tables)):
            sys.exit('# tables dont match # dates')
        
        for i in range(1, len(dates)):
            curr_date = dates[i]
            curr_table = show_tables[i]
            show_date = curr_date.find('b').text
            if(len(curr_table.find_all('td')) == 0):
               continue
            existing_shows_soup = list(curr_table.find_all('td'))

            for i in range(1, len(existing_shows_soup), 14):
                show_name = existing_shows_soup[i].text 
                show_time = existing_shows_soup[i-1].text 
                show_venue = existing_shows_soup[i+1].text 
                show_address = existing_shows_soup[i+2].text
                show_freq = existing_shows_soup[i+6].text
                show_cost = existing_shows_soup[i+7].text
                show_email = existing_shows_soup[i+9].find('a').get('href')
                show_hostname = existing_shows_soup[i+9].text
                show_website =  existing_shows_soup[i+10].find('a').get('href')
                show_phone = existing_shows_soup[i+11].text

                curr_show = Show(show_name, show_time, show_date, show_venue, show_address, show_freq, 
                                show_cost, show_email, show_website, show_phone, show_hostname )
                
                curr_cities_shows.append(curr_show)

        curr_city = City(soup_city.find('a').text, "https://badslava.com/" + soup_city.find('a').get('href'), curr_cities_shows)
        curr_cities.append(curr_city)
    curr_state = State(state_name, curr_cities, state_link)
    print(curr_state.name)
    all_states_data.append(curr_state)

all_shows = []

for state in all_states_data:
    for city in state.cities:
        for show in city.shows:
            show_info = {
                'state': state.name,
                'city': city.name,
                'show_name': show.name,
                'date': show.date,
                'time': show.time,
                'venue': show.venue
            }
            all_shows.append(show_info)


conn  = sqlite3.connect('us_mic_data.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS shows (
        show_id INTEGER PRIMARY KEY,
        state_name TEXT NOT NULL,
        city_name TEXT NOT NULL,
        show_name TEXT NOT NULL,
        show_date TEXT,
        show_time TEXT,
        show_venue TEXT
    )
''')

cursor.executemany('''
    INSERT INTO shows (state_name, city_name, show_name, show_date, show_time, show_venue)
    VALUES (:state, :city, :show_name, :date, :time, :venue)
''', all_shows)

conn.commit()
conn.close()
   




