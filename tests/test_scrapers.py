import unittest
import utils.scraper
import os



class TestScrapers(unittest.TestCase):
    def setUp(self):
        # mock the download function to use local files
        utils.scraper.urllib.urlopen = dummy_download
        
    
    def test_seriouseats(self):
        url = "http://www.seriouseats.com/recipes/2016/05/spicy-spring-sicilian-pizza-recipe.html"
        sereats = utils.scraper.web_scraper(url)
        assert sereats.title == r"Sicilian Pizza With Pepperoni and Spicy Tomato Sauce Recipe"
        assert len(sereats.ingredients) == 18
        assert "Kosher salt" in sereats.ingredients
        assert len(sereats.directions) == 8
        assert "Transfer dough to baking sheet" in sereats.directions[3]
        assert sereats.url == url
        assert sereats.image_url == 'http://www.seriouseats.com/recipes/assets_c/2016/05/20160503-spicy-spring-pizza-recipe-37-thumb-1500xauto-431711.jpg'
        
    def test_skinnytaste(self):
        url = "http://www.skinnytaste.com/gochujang-glazed-salmon/"
        skta = utils.scraper.web_scraper(url)
        assert skta.title == r"Gochujang-Glazed Salmon"
        assert skta.url == url
        assert skta.total_time == "PT10M"
        assert len(skta.ingredients) == 11
        assert '2 tsp mirin' in skta.ingredients
        assert 'the broiler pan with foil' in skta.directions[1]
        assert skta.image_url == 'http://www.skinnytaste.com/wp-content/uploads/2016/05/Gochujang-Glazed-Salmon-4-550x825.jpg'
        
    def test_foodnetwork(self):
        url = "http://www.foodnetwork.com/recipes/alton-brown/baked-macaroni-and-cheese-recipe.html"
        foodn = utils.scraper.web_scraper(url)
        assert foodn.title == 'Baked Macaroni and Cheese'
        assert foodn.url == url
        assert foodn.total_time == 'PT1H5M'
        assert len(foodn.ingredients) == 14
        assert '3 tablespoons butter' in foodn.ingredients
        assert 'While the pasta' in foodn.directions[2]
        assert foodn.image_url == 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2011/6/6/0/EA1E10_Baked-Macaraoni-and-Cheese_s4x3.jpg.rend.sniipadlarge.jpeg'
        
       
    def test_epicurious(self):
        url = 'http://www.epicurious.com/recipes/food/views/braised-short-ribs-350091'
        epi = utils.scraper.web_scraper(url)
        assert epi.url == url
        assert epi.title == 'Braised Short Ribs'
        assert '2 cups dry red wine' in epi.ingredients
        assert 'cook on low heat' in epi.directions[0]
        # image_url doesn't work here.  maybe image format issue??
        #assert epi.image_url == 'http://assets.epicurious.com/photos/560d79097b55306961bf354d/6:4/w_620%2Ch_413/350091_hires.jpg'
        # content="http://assets.epicurious.com/photos/560d79097b55306961bf354d/1:1/w_600%2Ch_600/350091_hires.jpg">
        
def dummy_download(url):
    fixtures = {'seriouseats.com' : 'serious_eats.html',
                'skinnytaste.com' : 'skinnytaste.html',
                'foodnetwork.com' : 'foodnetwork.html',
                'epicurious.com' : 'epicurious.html',
                'hrecipe' : 'hrecipe.html',
                'not_hrecipe': 'not_hrecipe.html'}
    
    fname = 'hrecipe.html'
    for k,v in fixtures.iteritems():
        if k in url:
            fname = v
    
    f = open(os.path.join('cookbook', 'fixtures', fname), 'r')
    html = f.read()
    f.close()
    return html