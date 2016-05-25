from bs4 import BeautifulSoup
import urllib


def web_scraper(url):
    """ Class factory function. Returns a scraper object based on the url """
    """ should first check if an hRecipe compliant site """
    html = download_url(url)
    if 'seriouseats' in url:
        return SeriousEatsScraper(html)
    elif 'skinnytaste' in url:
        return SkinnyTasteScraper(html)
    else:
        return GenericScraper(html)

def download_url(url):
    return urllib.urlopen(url)

    
class Scraper(object):

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
    
    @property
    def title(self):
        raise NotImplementedError

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
        
class SkinnyTasteScraper(Scraper):
    @property
    def title(self):
        return "SkinnyTaste Title"

class GenericScraper(Scraper):
    @property
    def directions(self):
        return "Generic Directions"