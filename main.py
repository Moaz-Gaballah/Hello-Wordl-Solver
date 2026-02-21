import json
from collections import Counter
import math


with open("dictionary_5_letter.json") as file:
    dict = json.load(file)
with open("targets_5_letter.json") as file:
    words = json.load(file)


def get_pattern(guess, answer):
    pattern = ['r', 'r', 'r', 'r', 'r']

    answer_trace = list(answer)

    for i in range(5):
        if guess[i] == answer[i]:
            pattern[i] = 'g'
            answer_trace[i] = None

    for i in range(5):
        if pattern[i] == 'r' and guess[i] in answer_trace:
            pattern[i] = 'y'
            answer_trace[answer_trace.index(guess[i])] = None

    return pattern

    



