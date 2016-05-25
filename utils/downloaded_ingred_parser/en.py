__author__ = 'sheraz/nibesh'

import re
from itertools import chain

from utils import normalize, escape_re_string

UNITS = {"cup": ["cups", "cup", "c.", "c"], 
         "fluid_ounce": ["fl. oz.", "fl oz", "fluid ounce", "fluid ounces"],
         "gallon": ["gal", "gal.", "gallon", "gallons"], 
         "ounce": ["oz", "oz.", "ounce", "ounces"],
         "pint": ["pt", "pt.", "pint", "pints"], 
         "pound": ["lb", "lb.", "pound", "pounds"],
         "quart": ["qt", "qt.", "qts", "qts.", "quart", "quarts"],
         "tbsp": ["tbsp.", "tbsp", "T", "T.", "tablespoon", "tablespoons", "tbs.", "tbs"],
         "tsp": ["tsp.", "tsp", "t", "t.", "teaspoon", "teaspoons"],
         "gram": ["g", "g.", "gr", "gr.", "gram", "grams"], 
         "kilogram": ["kg", "kg.", "kilogram", "kilograms"],
         "liter": ["l", "l.", "liter", "liters"], 
         "milligram": ["mg", "mg.", "milligram", "milligrams"],
         "milliliter": ["ml", "ml.", "milliliter", "milliliters"], 
         "pinch": ["pinch", "pinches", 'large pinch', 'Large pinch'],
         "dash": ["dash", "dashes"], 
         "touch": ["touch", "touches"], 
         "handful": ["handful", "handfuls"],
         "stick": ["stick", "sticks"], 
         "clove": ["cloves", "clove"], 
         "can": ["cans", "can"], 
         "large": ["large"],
         "small": ["small"], 
         "scoop": ["scoop", "scoops"], 
         "filets": ["filet", "filets"], 
         "sprig": ["sprigs", "sprig"],
         "inch" : ["inch", "inches"],
         "slices" : ["slice", "slices"]
        }

NUMBERS = {
           'zero': 0, 
           'one': 1, 
           'an': 1, 
           'a': 1,
           'two': 2,
           'three': 3, 
           'four': 4, 
           'five': 5, 
           'six': 6,
           'seven': 7,
           'eight': 8,
           'nine': 9, 
           'ten': 10, 
           'eleven': 11,
           'twelve': 12,
           'thirteen': 13, 
           'fourteen': 14,
           'fifteen': 15,
           'sixteen': 16,
           'seventeen' : 17,
           'eighteen': 18,
           'nineteen': 19,
           'twenty': 20,
           'thirty': 30,
           'forty': 40, 
           'fifty': 50,
           'sixty': 60, 
           'seventy': 70,
           'eighty': 80,
           'ninety': 90
           }

prepositions = ["of"]

a = list(chain.from_iterable(UNITS.values()))
a.sort(key=lambda x: len(x), reverse=True)
a = map(escape_re_string, a)

PARSER_RE = re.compile(
    r'(?P<quantity>(?:[\d\.,][\d\.,\s/]*)?\s*(?:(?:%s)\s*)*)?(\s*(?P<unit>%s)\s+)?(\s*(?:%s)\s+)?(\s*(?P<name>.+))?' % (
        '|'.join(NUMBERS), '|'.join(a), '|'.join(prepositions)))


def parse(st):
    """

    :param st:
    :return:
    """
    st = normalize(st)
    s = st.split()
    if NUMBERS.has_key(s[0].lower()):
        s[0] = str(NUMBERS[s[0].lower()])
        st = ' '.join(s)
        
    res = PARSER_RE.match(st)
    parsed = {}
    
    u = res.group('unit')
    if u:
        for k,v in UNITS.items():
            if u.lower().strip() in v:
                #print "Updating unit:  was: {}  now: {}".format(u,k)
                parsed['unit'] = k
    
    if not parsed.has_key('unit'):
        parsed['unit'] = res.group('unit') or ''
        
    parsed['quantity'] = res.group('quantity') or ''
    parsed['name'] = (res.group('name') or '').strip()
    #print parsed
    return parsed
