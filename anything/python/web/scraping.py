from bs4 import BeautifulSoup
import requests


html = requests.get('https://www.python.org')
soup = BeautifulSoup(html.text, 'lxml')

titles = soup.find_all('title')
print(titles[0].text)

intro = soup.find_all('div', {'class': 'introduction'})
print(intro[0].text)
