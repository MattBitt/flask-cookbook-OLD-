import unittest
from utils.scraper import SeriousEatsScraper



class TestScrapers(unittest.TestCase):
    def test_seriouseats(self):
        url = "http://www.seriouseats.com/recipes/2016/05/spicy-spring-sicilian-pizza-recipe.html"
        sereats = SeriousEatsScraper(url)
        print sereats.title
        assert sereats.title == r"Sicilian Pizza With Pepperoni and Spicy Tomato Sauce Recipe"
        #assert "Kosher salt" in sereats.ingredients
        for d in sereats.directions:
            print d.strip() + "\n"
        assert "Transfer dough to baking sheet" in sereats.directions