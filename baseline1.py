'''
Created by Claudia Naughton on 2019/05/07.
Simple baseline model for question answering.
Given a question and context, uses random guessing to output a unigram potential answer
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
