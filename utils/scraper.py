from bs4 import BeautifulSoup
import urllib


class Scraper(object):

    def __init__(self, url):
        self.soup = BeautifulSoup(self.download_url(url), 'html.parser')
        self.url = url
        

    def download_url(self, url):
        html = urllib.urlopen(url)
        return html
    

class SeriousEatsScraper(Scraper):
    
  
    @property
    def title(self):
        return self.soup.find('h1', {'class' : 'recipe-title'}).text

    @property 
    def ingredients(self):
        return self.get_list_contents('ingredient')

    @property
    def directions(self):
        return self.get_list_contents('recipe-procedure-text')
        
    
    def get_list_contents(self, class_name):
        list_items_with_tags = self.soup.find_all('div', {'class' : class_name})
        list_items = []
        for l in list_items_with_tags:
            list_items.append(l.text)
        return list_items