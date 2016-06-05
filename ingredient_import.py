import csv
import requests




if __name__ == "__main__":
    with open('ingredients.csv', 'rb') as csvfile:
        ingredients = csv.reader(csvfile, delimiter=',')
        for ingred, depart in ingredients:
            print 'ingred: {}    department:  {}'.format(ingred.lower(), depart.lower())
            payload = {'name' : ingred.lower(), 'department' : {'name' : depart.lower()}}
            r = requests.post('http://127.0.0.1:5000/ingredients/', json=payload)

