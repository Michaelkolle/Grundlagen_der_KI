from os import remove

import numpy as np


"""#Regeln: Es dürfen immer nur 2 Kreaturen auf dem Pferd sein.
#Es dürfen nie Mehr Orks als Elben auf den Seiten sein.

# Startzustand:
# Seite 1: 3 Orks 3 Elben
# Brücke/Pferd: 0 Kreaturen
# Seite 2: Keine Elben, Keine Orks

#Endzustand:
# Seite 1: Keine Leben und keine Orks
# Brücke/Pferd: 0 Kreaturen
# Seite 2: 3 Orks, 3 Elben"""

class Ork:
    pass


class Elbe:
    pass

ork1 = Ork
ork2 = Ork
ork3 = Ork

elbe1 = Elbe
elbe2 = Elbe
elbe3 = Elbe

side1 = [ork1, ork2, ork3, elbe1, elbe2, elbe3]

horse = []

side2 = []

def findOrk():
    for value in side1:
        if type(value) == Ork:
            side1.remove(value)
            return value
    return None


def findElbe():
    for value in side1:
        if type(value) == Elbe:
            side1.remove(value)
            return value
    return None


def my_solution():
    while not side1 and len(side2) < 5:

        if len(side1) == 5 and len(horse) < 1:
            horse.append(findOrk())


        if side2.count(type(Ork)) == side2.count(type(Elbe)) and len(horse) < 1:
            horse.append(findElbe())
        else: horse.append(findOrk())

        if type(Elbe) in horse and side2.count(type(Ork)) == type(Elbe):
            side2.append(type(Elbe) in horse)
            horse.remove(type(Elbe))




my_solution()
