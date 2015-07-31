'''
author: Jacob Egner
date: 2015-07-30
island: scientific expedition

puzzle URLs:
http://www.checkio.org/mission/einstein-problem/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-einstein-problem

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


import collections
import copy
import itertools


COLORS = set(['blue', 'green', 'red', 'white', 'yellow'])
PETS = set(['cat', 'bird', 'dog', 'fish', 'horse'])
BEVERAGES = set(['beer', 'coffee', 'milk', 'tea', 'water'])
CIGARETTES = set([
    'Rothmans', 'Dunhill', 'Pall Mall', 'Winfield', 'Marlboro'])
NATIONALITY = set(['Brit', 'Dane', 'German', 'Norwegian', 'Swede'])
NUMBERS = set(['1', '2', '3', '4', '5'])

QUESTIONS = set([
    "number", "color", "nationality", "beverage", "cigarettes", "pet"])

CATEGORIES = collections.OrderedDict([
    ('number', NUMBERS),
    ('color', COLORS),
    ('nationality', NATIONALITY),
    ('beverage', BEVERAGES),
    ('cigarettes', CIGARETTES),
    ('pet', PETS),
])

def answer(relations, question):
    persons = relationsToPersons(relations)
    mergePartialPersons(persons)
    fillInMissingTraits(persons)

    questionTrait, questionCategory = question.split('-')

    for person in persons:
        if questionTrait in person.values():
            return person[questionCategory]

    return "unknown"


def relationsToPersons(relations):
    persons = []

    for traitPair in relations:
        newPerson = dict(
            (traitToCategory(trait), trait)
            for trait in traitPair.split('-')
        )

        matchingPersons = []
        nextGeneration = []

        for person in persons:
            if set(newPerson.values()) & set(person.values()):
                newPerson.update(person)
            else:
                nextGeneration.append(person)

        nextGeneration.append(newPerson)
        persons = nextGeneration

    return persons


def traitToCategory(trait):
    for category, traits in CATEGORIES.items():
        if trait in traits:
            return category


def mergePartialPersons(persons):
    mergedPerson = True # will later become None and person-dict

    while mergedPerson:
        mergedPerson = None
        oldPersons = []

        for person1Idx, person1 in enumerate(persons):
            if len(person1) == len(CATEGORIES):
                continue
            for person2 in persons[person1Idx + 1:]:
                if len(person2) == len(CATEGORIES):
                    continue

                # if categories do not overlap
                if not(set(person1.keys()) & set(person2.keys())):
                    mergedPerson = person1.copy()
                    mergedPerson.update(person2)
                    oldPersons.append(person1)
                    oldPersons.append(person2)
                    break

            if mergedPerson:
                break

        if mergedPerson:
            for oldPerson in oldPersons:
                persons.remove(oldPerson)

            persons.append(mergedPerson)


def fillInMissingTraits(persons):
    categoryToMissingTraits = copy.deepcopy(CATEGORIES)

    for person in persons:
        for category, trait in person.items():
            categoryToMissingTraits[category].discard(trait)

    for person in persons:
        if len(person) < len(CATEGORIES):
            for category, missingTraits in categoryToMissingTraits.items():
                if missingTraits and category not in person:
                    person[category] = missingTraits.pop()


if __name__ == '__main__':
    assert answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
                   'German-coffee', 'beer-white', 'cat-water',
                   'horse-2', 'milk-3', '4-Rothmans',
                   'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
                   'bird-Brit', '4-green', 'Winfield-beer',
                   'Dane-blue', '5-dog', 'blue-horse',
                   'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
                  'fish-color') == 'green'  # What is the color of the house where the Fish lives?
    assert answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
                   'German-coffee', 'beer-white', 'cat-water',
                   'horse-2', 'milk-3', '4-Rothmans',
                   'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
                   'bird-Brit', '4-green', 'Winfield-beer',
                   'Dane-blue', '5-dog', 'blue-horse',
                   'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
                  'tea-number') == '2'  # What is the number of the house where tea is favorite beverage?
    assert answer(('Norwegian-Dunhill', 'Marlboro-blue', 'Brit-3',
                   'German-coffee', 'beer-white', 'cat-water',
                   'horse-2', 'milk-3', '4-Rothmans',
                   'dog-Swede', 'Norwegian-1', 'horse-Marlboro',
                   'bird-Brit', '4-green', 'Winfield-beer',
                   'Dane-blue', '5-dog', 'blue-horse',
                   'yellow-cat', 'Winfield-Swede', 'tea-Marlboro'),
                  'Norwegian-beverage') == 'water'  # What is the favorite beverage of the Norwegian man?
