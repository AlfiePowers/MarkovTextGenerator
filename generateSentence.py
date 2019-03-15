import numpy as np
from collections import defaultdict
import random


def make_dictionary():
    # Get all of the different words
    text = list()
    with open('text.txt', 'r') as f:
        for line in f:
            words = list()
            for word in line.split():
                words.append(word)
            text.append(words)

    dictionary = defaultdict(list)

    def add_to_dict(current, next):
        if current in dictionary:
            li = dictionary[current]
            in_list = False
            for x in range(0, len(li), 1):
                if li[x][0] == next:
                    in_list = True
            if in_list:
                for x in range(0, len(li), 1):
                    if li[x][0] == next:
                        li[x] = (next, li[x][1] + 1)
                dictionary[current] = li
            else:
                dictionary[current].append((next, 0))
        else:
            dictionary[current].append((next, 0))

    # Process the words into a dictionary
    for l in text:
        for w in range(0, len(l), 1):
            if w == len(l) - 1:
                add_to_dict(l[w], ".")
            else:
                add_to_dict(l[w], l[w + 1])

    np.save('dictionary.npy', dictionary)


def generate_sentence():
    read_dictionary = np.load('dictionary.npy').item()

    def get_next_word(previous, sentence):

        if previous != ".":
            sentence = sentence + " " + previous
            possible_words = list()
            for x in read_dictionary[previous]:
                for y in range(0, x[1] + 1, 1):
                    possible_words.append(x[0])
            next_word = random.choice(possible_words)
            return get_next_word(next_word, sentence)
        sentence = sentence
        return sentence

    starting_word = "america"
    try:
        sentence = get_next_word(starting_word, "")
    except IndexError:
        return "Failed to find starting word: " + starting_word
    return sentence


make_dictionary()
print(generate_sentence())
