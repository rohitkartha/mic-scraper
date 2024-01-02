import httpx
from bs4 import BeautifulSoup
import sqlite3

conn  = sqlite3.connect('us_mic_data.db')

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
  def __init__(self, name, time, venue, address, freq, cost, email, link, phone, hostname):
    self.name = name
    self.link = link
    self.time = time
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

#len(state_geounits)
for i in range(0, 1):
    curr_cities = [] 
    curr_state_soup = state_geounits[i]
    state_name = curr_state_soup.find('h3').find('a').text
    state_link = curr_state_soup.find('h3').find('a').get('href')
    
    soup_cities = list(curr_state_soup.find_all('li'))
    for soup_city in soup_cities:
        curr_city_req = httpx.get("https://badslava.com/" + soup_city.find('a').get('href'))
        curr_city_soup= BeautifulSoup(curr_city_req.text, 'html.parser')
        curr_cities_shows = []

        shows_soup = list(curr_city_soup.find_all("td"))
        for i in range(1, len(shows_soup), 14):
            show_name = shows_soup[i].text 
            show_time = shows_soup[i-1].text 
            show_venue = shows_soup[i+1].text 
            show_address = shows_soup[i+2].text
            show_freq = shows_soup[i+6].text
            show_cost = shows_soup[i+7].text
            show_email = shows_soup[i+9].find('a').get('href')
            show_hostname = shows_soup[i+9].text
            show_website =  shows_soup[i+10].find('a').get('href')
            show_phone = shows_soup[i+11].text

            curr_show = Show(show_name, show_time, show_venue, show_address, show_freq, 
                             show_cost, show_email, show_website, show_phone, show_hostname )
            
            curr_cities_shows.append(curr_show)

        curr_city = City(soup_city.find('a').text, "https://badslava.com/" + soup_city.find('a').get('href'), curr_cities_shows)
        curr_cities.append(curr_city)
    curr_state = State(state_name, curr_cities, state_link)
    all_states_data.append(curr_state)

