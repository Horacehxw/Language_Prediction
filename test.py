import unittest
from util import Country

class MyTestCase(unittest.TestCase):
    def test_update(self):
        canada = Country("English", "French", 0.68, 0.126, 0.175, 0.7, 0.3, 0.5,
                         Pop = [10000])
        for _ in range(100):
            canada.update()

    def test_grow(self):
        canada = Country("English", "French", 0.68, 0.126, 0.175, 0.7, 0.3, 0.5,
                         Pop=range(10000, 30000, 1000))
        for _ in range(11000, 30000, 1000):
            canada.update()
            canada.grow()

    def test_transmit(self):
        canada = Country("English", "French", 0.68, 0.126, 0.175, 0.7, 0.3, 0.5,
                         Pop=range(10000, 30000, 1000))
        us = Country("Spain", "English",  0.5, 0.3, 0.2, 0.4, 0.7, 0.75,
                         Pop=range(10000, 30000, 1000))
        china = Country("Chinese", None, 1, 0, 0, 1, 0, 0,
                     Pop=range(10000, 30000, 1000))
        us.transmit(canada, 0.1)
        canada.transmit(china, 0.1)
        print('hello')

    def test_language(self):
        import pandas as pd
        import numpy as np
        # read data to calculate the similarity coeficient (0.25, 0.5, 0.75)
        language = pd.read_csv('../data/languages by Population and family.csv').dropna(axis=0, how='all')
        list_language = list(language['Language'].values)
        language.insert(2, 'familys', [[f.strip() for f in l.split(",")] for l in language['language family'].values])
        similarity = np.zeros((len(list_language), len(list_language)))
        for i in range(len(list_language)):
            for j in range(len(list_language)):
                if i == j:
                    similarity[i, j] = 1
                else:
                    family_i = language[language['Language'] == list_language[i]]['familys'].values[0] # get the real element.
                    family_j = language[language['Language'] == list_language[j]]['familys'].values[0]
                    if family_i[0] != family_j[0]:
                        similarity[i, j] = 0.25
                    elif len(family_i) > 1 and len(family_j) > 1:
                        if family_i[1] != family_j[1]:
                            similarity[i, j] = 0.5
                        else:
                            print("{},{}".format(i, j))
                            similarity[i, j] = 0.75
                    else:
                        similarity[i, j] = 0.5

if __name__ == '__main__':
    unittest.main()
