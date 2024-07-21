import collections
from random import choice

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]
    
deck = FrenchDeck()

# print(choice(deck))
# print(len(deck))
# print(deck[12::13])
# print(deck[0])
# print(Card('Q', 'beasts') in deck)


suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


# print("NOT sorted cards")
# for card in deck:
#     print(card)

# print("sorted cards")
# for card in sorted(deck, key=spades_high, reverse=True): 
#     print(card)


my_list = ["milk", "bread", "apples"]

""" sort(), sorted(), iter(), reverse()"""    
# i_list = iter(my_list)
# for item in i_list:
#     print(item)

# r_list = reversed(my_list)
# for item in r_list:
#     print(item)

# my_list.reverse()
# print(my_list[0])

import math

class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x!r}, {self.y!r})'

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


v1 = Vector(2, 4)
v2 = Vector(2, 1)
v3 = v1 + v2
# print(v1 + v2)
# print(abs(v3))
# print(v1)
# print(v1*-1)

thisset = set(("apple", "banana", "cherry"))
thisset.add("blueberry")
thisset.remove("banana")
#print(thisset)

fruits = {"apple", "banana", "cherry"}
more_fruits = ["orange", "mango", "grapes"]
#print(fruits.union(more_fruits))

import numpy as np

# arr = np.array([1, 2, 3, 4], ndmin=5)
# print(arr)
# print('shape of array :', arr.shape)

# arr = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])

# for x in np.nditer(arr, flags=['buffered'], op_dtypes=['S']):
#   print(x)

# for idx, x in np.ndenumerate(arr):
#   print(idx, x)

# arr1 = np.array([[1, 2], [3, 4]])
# arr2 = np.array([[5, 6], [7, 8]])
# arr = np.concatenate((arr1, arr2), axis=1)
# print(arr)

# arr = np.array([1, 2, 3, 4, 5, 6])
# newarr = np.array_split(arr, 3)
# print(newarr)

# traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]
# for passport in sorted(traveler_ids):
#     print('%s/%s' % passport) 
#     print(f"{passport[0]}/{passport[1]}")

# *head, b, c, d = range(5)
# print(head, b, c, d)

metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]

def main():
    print(f'{"":15} | {"latitude":9} | {"longitude":9}')
    for name, _, _, (lat, lon) in metro_areas:
        if lon <= 0:
            print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')

if __name__ == '__main__':
    main()