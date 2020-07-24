import requests # for making standard html requests
from bs4 import BeautifulSoup # magical tool for parsing html data
import json # for parsing data



url='https://www.google.com/search?q=good+news+coronavirus&rlz=1C1CHBD_enIN903IN903&source=lnms&tbm=nws&sa=X&ved=2ahUKEwj904fqz9TqAhVQyjgGHZ-wDjUQ_AUoAXoECAwQAw&biw=1366&bih=625'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
tag = soup.find_all('div', attrs={'class':'BNeawe vvjwJb AP7Wnd'})
for i in tag:
    print(i.get_text())