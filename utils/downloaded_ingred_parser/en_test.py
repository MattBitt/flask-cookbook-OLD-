import unittest

import en as ip


class TestIngredientParserSwedish(unittest.TestCase):
    def setUp(self):
        self.teststrings = [
            '1 mg saffran',
            '1mg saffran',
            '1                               mg saffran',
            '1 \n\r \n\r       mg saffran',
            '1 mg                            saffran',
            '1             mg            saffran',
            '1      \r\n       mg  \r\n          saffran',
        ]

    def test_normalize_whitespace(self):
        for s in self.teststrings:
            self.assertEqual('1 mg saffran', ip.normalize(s))

        res = ip.normalize('11/12   mg   saffran')
        self.assertEqual('11/12 mg saffran', res)

    def test_integer_and_metric_weight_with_whitespace_inbetween(self):
        for s in self.teststrings:
            res = ip.parse(s)
            self.assertEqual('1 mg', res['measure'])
            self.assertEqual('saffran', res['name'])

        res = ip.parse('1 g saffran')
        self.assertEqual('1 g', res['measure'])
        self.assertEqual('saffran', res['name'])

        res = ip.parse('200 gram something')
        self.assertEqual('200 gram', res['measure'])
        self.assertEqual('something', res['name'])

    def test_fractions_and_metric_weight_with_whitespace_inbetween(self):

        res = ip.parse('1/2   mg   saffran')
        self.assertEqual('1/2 mg', res['measure'])
        self.assertEqual('saffran', res['name'])

        res = ip.parse('1/2mg   saffran')
        self.assertEqual('1/2 mg', res['measure'])
        self.assertEqual('saffran', res['name'])

        res = ip.parse('11/12   mg   saffran')
        self.assertEqual('11/12 mg', res['measure'])
        self.assertEqual('saffran', res['name'])

        res = ip.parse('11/12mg   saffran')
        self.assertEqual('11/12 mg', res['measure'])
        self.assertEqual('saffran', res['name'])

        res = ip.parse('7 1/2 dl mjol')
        self.assertEqual('7 1/2 dl', res['measure'])
        self.assertEqual('mjol', res['name'])

    def test_decimals_and_metric_weight_with_whitespace_inbetween(self):
        res = ip.parse('1.5   mg   saffran')
        self.assertEqual('1.5 mg', res['measure'])
        self.assertEqual('saffran', res['name'])

        res = ip.parse('1,5mg   saffran')
        self.assertEqual('1,5 mg', res['measure'])
        self.assertEqual('saffran', res['name'])

    def test_no_measurement(self):
        res = ip.parse('salt och peppar')
        self.assertEqual('', res['measure'])
        self.assertEqual('salt och peppar', res['name'])

    def test_qty_but_no_measurement(self):
        res = ip.parse('3 red   peppar')
        self.assertEqual('3', res['measure'])
        self.assertEqual('red peppar', res['name'])

    def test_approximation_measurements(self):
        res = ip.parse('300 ca g farsk   lammkorv')
        self.assertEqual('300 ca g', res['measure'])
        self.assertEqual('farsk lammkorv', res['name'])


if __name__ == '__main__':
    #unittest.main()
    ingreds = ['4 baby bok choy',
               '4 cloves garlic',
               '1 pound shiitake mushrooms',
               '1 inch knob fresh ginger',
               '1/2 cup chicken or vegetable stock',
               '1 teaspoon cornstarch',
               '1  tablespoon mirin', 
               '1 teaspoon sesame oil',
               '1/4 teaspoon crushed red pepper',
               '1/2 pounds shrimp, peeled and deveined',
               '1 teaspoon kosher salt',
               'freshly ground black pepper']
    ingreds = """4 baby bok choy
4 cloves garlic
1 pound shiitake mushrooms
1 inch knob fresh ginger
1/2 cup chicken or vegetable stock
1 teaspoon cornstarch
1  tablespoon mirin
1 teaspoon sesame oil
1/4 teaspoon crushed red pepper
1/2 pounds shrimp, peeled and deveined
1 teaspoon kosher salt 
freshly ground black pepper
3 slices center-cut bacon, diced
3 cups shredded brussels sprouts
thirty oz avocado, diced (1 small)
1 tsp dijon mustard
4 tsp olive oil
2 tbsp plus 1 tsp red wine vinegar
2 tablespoons chopped red onion
1/2 teaspoon kosher salt
24 oz lean boneless pork chops
4 cloves garlic, crushed
1/2 tsp cumin
1/2 tsp chili powder
1/2 tsp paprika
1/2 lime
1 tsp lime zest
1 teaspoon kosher salt and fresh pepper
1 1/2 pounds fresh fava bean pods
Kosher salt
2 small carrots, with a small handful of their tenderest greens if available
2 tablespoons extra-virgin olive oil, plus more for drizzling
One tablespoon fresh juice from 1 lemon, 
1 Large pinch of grated zest
1 small shallot thinly sliced
Freshly ground black pepper
6 ounces high-quality ricotta cheese
4 slices hearty toast"""
    ingreds_list = [i.strip() for i in ingreds.split('\n')]


    for i in ingreds_list:
        res = ip.parse(i)
        #print res
        #for k, v in ip.UNITS.items():
            #print k, v
        #    if res['unit'] in v:
        #        res['unit'] = k
        print res['quantity'] + '\t' + res['unit'] + '\t' + res['name']        
      
