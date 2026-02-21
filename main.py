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

    
def calc_entropy(guess, words):

    pattern_count = Counter()

    for word in words:
        pattern = get_pattern(guess, word)

        pattern_count[pattern] +=1

    entropy = 0
    length = len(words)

    for count in pattern_count.values():

        p = count / length

        entropy += -p * math.log2(p)

    return entropy

def best_guesses(guess, ansewrs):
    result = []

    for word in guess:
        entropy = calc_entropy(word,ansewrs)
        result.append({
            "word" : word,"entropy": entropy, "possible_Ans": word in ansewrs
        })

    result.sort(key=lambda x: x["entropy"], reverse=True)

    return result[:20]

def filtration(guess, pattern, words):

    for word in words:
        if get_pattern(guess, word) != pattern:
            words.remove(word)
    return words 