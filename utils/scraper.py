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
    elif 'foodnetwork' in url:
        return FoodNetworkScraper(html)
    else:
        if 'hrecipe' in html:
            return GenericHRecipeScraper(html)
        else:
            ####################### never reaching this point ################
            print "Should see error"
            # should be a custom error that I catch above
            raise NameError

def download_url(url):
    return urllib.urlopen(url)

    
class Scraper(object):

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
    
    @property
    def title(self):
        return self.soup.find('meta', {'property' : 'og:title'}).get('content')
    
    @property
    def ingredients(self):
        raise NotImplementedError
    
    @property
    def directions(self):
        raise NotImplementedError
    
    @property
    def url(self):
        return self.soup.find('meta', {'property' : 'og:url'}).get('content')

    def get_list_contents(self, tag, class_name):
        list_items_with_tags = self.soup.find_all(tag, {'class' : class_name})
        list_items = []
        for l in list_items_with_tags:
            list_items.append(l.text)
        return list_items

    @property
    def image_url(self):
        return self.soup.find('meta', {'property' : 'og:image'}).get('content') 
        
class SeriousEatsScraper(Scraper):
    @property 
    def ingredients(self):
        return self.get_list_contents('li', 'ingredient')

    @property
    def directions(self):
        return self.get_list_contents('div', 'recipe-procedure-text')

        
class SkinnyTasteScraper(Scraper):
    @property
    def total_time(self):
        return self.soup.find('meta', {'itemprop' : 'totalTime'}).get('content')
        
    @property
    def ingredients(self):
        list_items_with_tags = self.soup.find_all('li', {'itemprop' : 'ingredients'})
        list_items = []
        for l in list_items_with_tags:
            list_items.append(l.text)
        return list_items  
        
    @property
    def directions(self):
        list_items_with_tags = self.soup.find('span', {'itemprop' : 'recipeInstructions'}).find('ol').find_all('li')
        list_items = []
        for l in list_items_with_tags:
            list_items.append(l.text)
        return list_items 


class GenericHRecipeScraper(Scraper):
    @property
    def directions(self):
        return "Generic Directions"
        
        
class FoodNetworkScraper(Scraper):
    @property
    def title(self):
        return self.soup.find('div', {'class' : 'title'}).find('h1').text
    
    @property
    def total_time(self):
        return self.soup.find('meta', {'itemprop' : 'totalTime'}).get('content')
        
    @property
    def ingredients(self):
        list_items_with_tags = self.soup.find_all('li', {'itemprop' : 'ingredients'})
        list_items = []
        for l in list_items_with_tags:
            list_items.append(l.text)
        return list_items
        
    @property
    def directions(self):
        list_items_with_tags = self.soup.find('ul', {'class' : 'recipe-directions-list'}).find_all('li')
        list_items = []
        for l in list_items_with_tags:
            list_items.append(l.find('p').text)
        return list_items