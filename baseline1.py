'''
Simple baseline model for question answering
Given a question and context, uses random guessing to output a potential answer
TODO: tokenization step with api tokenizer
Should the potential answers be sentences, phrases, or words? (or all three?)
'''

import load_data
import random
from random import randint
import nltk


global _TOKENIZER
_TOKENIZER = nltk.tokenize.casual.TweetTokenizer(
    preserve_case=False)

def tokenize(string):
    global _TOKENIZER
    return _TOKENIZER.tokenize(string)

def get_answer(paragraph, question):
    tokens = tokenize(paragraph)
    random.seed(1)
    index = random.randint(0, len(tokens) - 1)

    return tokens[index]
