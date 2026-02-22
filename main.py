import json
from collections import Counter
import math
import pickle
import os


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



first_guess_file = "first_guesses.pkl"

if os.path.exists(first_guess_file):
    print("Loading precomputed first guess rankings...")
    with open(first_guess_file, "rb") as f:
        first_guess_ranking = pickle.load(f)
else:
    print("Computing first guess rankings...")
    first_guess_ranking = []
    for word in dict:
        pattern_count = Counter(get_pattern(word, answer) for answer in words)
        total = len(words)
        entropy = sum(-(c / total) * math.log2(c / total) for c in pattern_count.values())
        first_guess_ranking.append({
            "word": word, "entropy": entropy, "possible_Ans": word in words
        })
    first_guess_ranking.sort(key=lambda x: x["entropy"], reverse=True)
    with open(first_guess_file, "wb") as f:
        pickle.dump(first_guess_ranking, f)
    
    
def calc_entropy(guess, words):

    pattern_count = Counter(get_pattern(guess, word) for word in words)
    total = len(words)
    return sum(-(c / total) * math.log2(c / total) for c in pattern_count.values())

def best_guesses(words):
    result = []

    for word in dict:
        entropy = calc_entropy(word,words)
        result.append({
            "word" : word,"entropy": entropy, "possible_Ans": word in words
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

        print(f"{rank:>2}. {word} \t entrtopy = {entropy: .3f}")

def filtration(guess, pattern, words):

    return [word for word in words if get_pattern(guess, word) == pattern] 

def get_input_pattern():
    print("Now Enter the pattern (r = grey, y = yellow, g = green)")
    
    while True:
        pattern = list(input(">> ").lower())
        
        if len(pattern) == 5 and all(c in "ryg" for c in pattern):
            return tuple(pattern)
        print("Please enter a valid pattern")


# Main loop and execution

print("\t\t\t \t \t \t Welcome To Hello Wordl Solver")

current_attempt = 0

while current_attempt < 6:

    if(len(words) == 1):
        print(f"The Answer is: {words[0]}")
        break

    if(current_attempt != 0): print("Calculating best guesses ...")


    print(f"============ Round {current_attempt +1} ============")


    if current_attempt == 0:
        display_guesses(first_guess_ranking[:20])
    else:
        display_guesses(best_guesses(words))

    print("-" * 36)

    while True:
        gussed_word = input("Enter the gussed word: ")
        if gussed_word in dict: break
    pattern = get_input_pattern()
    words = filtration(gussed_word, pattern, words)

    if pattern == ('g', 'g', 'g', 'g', 'g'):
        break

    current_attempt +=1