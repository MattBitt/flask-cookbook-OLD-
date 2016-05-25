import unittest
from utils.scraper import web_scraper



class TestScrapers(unittest.TestCase):
    def test_seriouseats(self):
        url = "http://www.seriouseats.com/recipes/2016/05/spicy-spring-sicilian-pizza-recipe.html"
        sereats = web_scraper(url)
        #print sereats.title
        assert sereats.title == r"Sicilian Pizza With Pepperoni and Spicy Tomato Sauce Recipe"
        assert "Kosher salt" in sereats.ingredients
        #for d in sereats.directions:
        #    print d.strip() + "\n"
        assert "Transfer dough to baking sheet" in sereats.directions
        
    def test_skinnytaste(self):
        url = "http://www.skinnytaste.com/gochujang-glazed-salmon/"
        skta = web_scraper(url)
        #print skta.title
        assert skta.title == r"SkinnyTaste Title"
        #assert "Kosher salt" in sereats.ingredients
        #for d in sereats.directions:
        #    print d.strip() + "\n"
        #assert "Transfer dough to baking sheet" in sereats.directions
        
    def test_other(self):
        url = "http://www.foodnetwork.com/recipes/marcela-valladolid/baja-style-fish-tacos-recipe.html"
        other = web_scraper(url)
        print other.title

        