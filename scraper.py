import httpx
from bs4 import BeautifulSoup

class state:
  def __init__(self, name, cities):
    self.name = name
    self.cities = cities


class city:
  def __init__(self, name, link):
    self.name = name
    self.link = link
   

r = httpx.get('https://badslava.com/open-mics-state.php?state=NC&type=Comedy')
soup = BeautifulSoup(r.text, 'html.parser')
print(len(list(soup.find_all("td"))))

for i in range(1, 406, 14):  # Starting from 1, increment by 8 until less than 50
    print(list(soup.find_all("td")[i]))

#print(len(list(soup.children)))
    
main_page = httpx.get('https://badslava.com/')
soup = BeautifulSoup(main_page.text, 'html.parser')
united_states_geoblock = (soup.find('div', class_='united-states'))

state_geounits = list(united_states_geoblock.find_all('div', class_='geoUnit'))

all_states_data = []

for i in range(0, 1):
    curr_cities = [] 
    curr_state_soup = state_geounits[i]
    state_name = curr_state_soup.find('h3').find('a').text
    
    cities = list(curr_state_soup.find_all('li'))
    for city in cities:
        curr_city = city(city.find('a').text, city.find('a').get('href'))
        print(city.find('a').get('href')) 
    #print(cities)
    #print(curr.find('a').get('href'))
