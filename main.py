import json
from collections import Counter
import math


with open("dictionary_5_letter.json") as file:
    dict = json.load(file)
with open("targets_5_letter.json") as file:
    words = json.load(file)


# Functions definitions

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

    return tuple(pattern)

    
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

def display_guesses(guesses):

    print("Top suggestions:")

    for i,j in enumerate(guesses):
        rank = i+1
        word = j["word"].upper()
        entropy = j["entropy"]
        possible = j["possible_Ans"]

        print(f"{rank}. {word} \t entrtopy = {entropy: .3f} \t possibility = {possible}")

def filtration(guess, pattern, words):

    return [word for word in words if get_pattern(guess, word) == pattern] 

def get_input_pattern(guess):
    print(f"You guessed {guess}")
    print("Now Enter the pattern (r = grey, y = yellow, g = green)")
    
    while True:
        pattern = list(input().lower())
        
        if len(pattern) == 5 and all(c in "ryg" for c in pattern):
            return tuple(pattern)
        print("Please enter a valid pattern")


# Main loop and execution

print("\t\t\t \t \t \t Welcome To Hello Wordl Solver")

current_attempt = 0

while current_attempt < 6:

    if(len(words) == 1):
        print(f"Answer must be {words[0]}")
        break

    print(f"===== Round {current_attempt +1} =====")

    print("Calculating best guesses ...")

    display_guesses(best_guesses(dict, words))

    while True:
        gussed_word = input("Enter the gussed word: ")
        if gussed_word in dict: break
    pattern = get_input_pattern(gussed_word)
    words = filtration(gussed_word, pattern, words)

    if pattern == ('g', 'g', 'g', 'g', 'g'):
        print(f"Solved in {current_attempt + 1} attempts!")
        break

    current_attempt +=1