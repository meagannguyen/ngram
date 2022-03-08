# Name: Meagan Nguyen
# CMSC 416: Introduction to NLP
# Date: March 08, 2022
# Programming Assignment 2: n-grams


# The n-gram model is a language modeling algorithm that utilizes probability and computational linguistics for Natural Language Processing
# procedures such as word prediction. When fed in raw text, n-grams produce sequences of n number of separated symbols or tokens, where each
# sequence is adjacent to each other. For example, considering the phrase "I like to watch anime.", if n is defined to be 2, we can generate
# 2-grams, or bigrams, which are
# (I like), (like to), (to watch), (watch anime), (anime .)
# If n is defined to be 3, we can generate 3-grams, or trigrams, which are
# (I like to), (like to watch), (to watch anime), (watch anime .)
# Each sequence is contains a "subset" of its neighboring sequence. In this project, we separate and therefore tokenize punctuation alongside
# alphanumeric values. This project specifically utilizes an n-gram model to calculate the likelihood of the next token to be produced and
# generated based off of conditional probability.


# Algorithm:
#   1. Read in command-line arguments from prompt in format: python ngram.py n m input-file(s)
#       a. n is the value for n in n-grams
#       b. m specifies how many sentences for the model to output
#       c. input-file(s) are text files
#   2. Break open and read raw text for every input text file
#   3. Make the entire text lowercase
#   4. Call function get_corpus that takes in raw text and tokenizes text into a corpus list
#   5. Call function get_ngrams that takes in corpus and specified n and generates n-grams of the corpus
#   6. Call function get_ngram_frequencies that takes in the list of n-grams and returns ngram_frequencies dictionary to store n-gram counts
#       a. Initializes empty ngram_frequencies dictionary
#       b. Assigns word variable as the last word of the n-gram
#       c. Assigns history to all the contents of n-gram before word
#       d. Checks if history and word are not in ngram_frequencies dictionary to add it
#       e. If they are found in the dictionary, increment the count of each n-gram
#   7. Generate a random choice from list of n-gram keys as next token
#   8. For the user-specified number of sentences:
#       a. Call generate_next_token function
#           i. Sums the weight of each candidate token
#           ii. Selects a random arbitrary weight
#           iii. Loop through list of candidate tokens
#           iv. Increment counter by randomly generated weight 
#           v. If counter is greater than random then generate that candidate token
#       b. If the rndom generated token is either a ., ?, or !, add new line and move to next sentence
#   9. Print correctly formatted m-number of sentences


# Usage:
#   python ngram.py n m input-file(s)
#   where n specifies the n in n-grams, m is the number of sentences to generate and n and m are integers

##########################################################################################################


import sys
import re
import random


# tokenizes and normalizes entire corpus of raw text
def get_corpus(raw_text):
    # removes all non-alphabetical letters, spaces and new lines
    raw_text = re.sub(r'[^\w\s\n?.—!-\']', '', raw_text)
    # replaces new line delimiter with a space
    raw_text = raw_text.replace('\n', ' ')
    # replaces underscores with a space
    raw_text = raw_text.replace("_", " ")
    # replaces hyphens with a space
    raw_text = raw_text.replace("-", " ")
    raw_text = raw_text.replace("—", " ")
    # adds whitespace around periods
    raw_text = raw_text.replace(".", " . ")
    # adds whitespace around question marks
    raw_text = raw_text.replace("?", " ? ")
    # adds whitespace around exclamation points
    raw_text = raw_text.replace("!", " ! ")
    corpus = ' '.join(raw_text.split())
    return corpus


# calculates n-grams for model
def get_ngrams(corpus, n):
    ngrams = [corpus[i:i + int(n)] for i in range(len(corpus) - int(n) + 1)]
    return ngrams


# function to store previously seen n-grams
def get_ngram_frequencies(ngrams):
    ngram_frequencies = {}
    for ngram in ngrams:
        # sets history as n-1 of each n-gram
        history  = " ".join(ngram[:-1])
        # sets word as last element of each n-gram
        word = ngram[-1]
        # if history is not found in dict then add to dict
        if history not in ngram_frequencies:
            ngram_frequencies[history] = {}
        # if word is not found in dict with corresponding history then initialize count to 0
        if word not in ngram_frequencies[history]:
            ngram_frequencies[history][word] = 0
        # incrememnt count for each history and corresponding word to store in dict
        ngram_frequencies[history][word] += 1.0
    return ngram_frequencies


# function to generate random next token
def generate_next_token(text, n, ngram_frequencies):
    # sets history as already seen text
    history = " ".join(text.split()[-(int(n) - 1):])
    # initializes list of candidate tokens
    candidates = ngram_frequencies[history].items()
    # adds up all the weights for potential candidates
    weight_sum = sum(weight for candidate, weight in candidates)
    # generates a random weight between 0 and calculated sum of weights
    rand = random.uniform(0, weight_sum)
    counter = 0
    for candidate, weight in candidates:
        counter += weight
        if counter > rand: 
            return candidate


# function to correctly reformat output sentence(s)
def reformat_sentence(text):
    # removes whitespace between end of sentence delimiter and previous token
    text = re.sub(r'\s+([.?!"])', r'\1', text)
    # capitalizes very first word of generated text in sentence
    text = text.capitalize()
    # capitalizes first word of every sentence
    text = re.sub('([.!?]\\s+[a-z])', lambda c: c.group(1).upper(), text)
    return text


def main():
    # first arg is n in n-gram
    n = sys.argv[1]
    # second arg is the number of sentences
    m = sys.argv[2]
    numArgs = len(sys.argv)
    # for all text file arguments
    for i in range(3, numArgs):
        textFile = sys.argv[i]
        # break open text file args and read contents
        with open(textFile, 'r') as f:
            raw_text = f.read()
            print("\nThis program generates random sentences based off an n-gram model.\n")
            print("Command line settings: ngram.py " + n + ' ' + m + '\n')
            # makes entirety of raw text lowercase
            raw_text = raw_text.lower()
            corpus = get_corpus(raw_text)
            ngrams = get_ngrams(corpus.split(" "), n)
            ngram_frequencies = get_ngram_frequencies(ngrams)
            next_token = random.choice(list(ngram_frequencies.keys()))
            #next_token = next_token.lower();
            sentences = 0
            while sentences < int(m):
                next_token += " " + generate_next_token(next_token, n, ngram_frequencies)
                if next_token.endswith(('.','?', '!')): 
                    next_token += '\n'
                    sentences += 1 
            print(reformat_sentence(next_token))

main()