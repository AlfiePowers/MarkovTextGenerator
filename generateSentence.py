import numpy as np
from collections import defaultdict
import random


def make_dictionary():
    # Retrieve the training sentences from a file
    text = list()
    with open('trainingData/text.txt', 'r') as f:
        for line in f:
            # Convert the line values into lists of lists of words
            words = list()
            for word in line.split():
                words.append(word)
            text.append(words)

    dictionary = defaultdict(list)

    # Add to dictionary should create a new list entry in the case that the first word has not been seen in the
    # dictionary. It should also add the second word into the dictionary but as the amount of occurances that has
    # previously been seen + 1 (starting at 0)
    # If the second word is in the dictionary, we should increment the value once again.
    def add_to_dict(current, next):
        # Sanity check to ensure that the value is in the dictionary
        # We could essentially ignore this but it is safer and will lead to less type errors
        if current in dictionary:
            li = dictionary[current]

            # Our implementation of is in list. As the list is not ordered we should assume that the best we can do
            # is an implementation that loops through the entire list. Could order this with a hashmap but potential
            # memory overhead plus this dictionary need only be generated once.
            in_list = False
            for x in range(0, len(li), 1):
                if li[x][0] == next:
                    in_list = True

            # Checks if the second word is in the list, incrementing if it is, else adding a 1 entry.
            if in_list:
                for x in range(0, len(li), 1):
                    if li[x][0] == next:
                        li[x] = (next, li[x][1] + 1)
                dictionary[current] = li
            else:
                dictionary[current].append((next, 1))
        else:
            dictionary[current].append((next, 1))

    # We loop through all of the words and add to the dictionary with the next word if it is not blank
    for l in text:
        for w in range(0, len(l), 1):
            if w == len(l) - 1:
                add_to_dict(l[w], ".")
            else:
                add_to_dict(l[w], l[w + 1])

    np.save('output/dictionary.npy', dictionary)


# This generates the sentence given a starting word
def generate_sentence():
    # Reads the dictionary from memory ensuring it exists
    try:
        read_dictionary = np.load('output/dictionary.npy').item()
    except FileNotFoundError:
        make_dictionary()
        read_dictionary = np.load('output/dictionary.npy').item()

    # This function given a word will find the next possible word in the sequence. Done by generating a list of all
    # of the possible words with words repeated given how often they show up
    def get_next_word(previous, sentence):
        # Ensure that there is a next word to be read
        if previous != ".":
            sentence = sentence + " " + previous
            possible_words = list()
            for x in read_dictionary[previous]:
                for y in range(0, x[1] + 1, 1):
                    possible_words.append(x[0])
            next_word = random.choice(possible_words)
            # Recursively call until we have met the condition of an end word
            return get_next_word(next_word, sentence)
        sentence = sentence
        return sentence

    # A base starting word
    starting_word = "america"

    # We need to specify the starting word and the current sentence
    try:
        sentence = get_next_word(starting_word, "")
    except IndexError:
        # If we can't find a word in the dictionary, we can't start. There is no training data
        # TODO: Implement a way of finding the next closest word to the current value
        return "Failed to find starting word: " + starting_word
    return sentence

print(generate_sentence())
