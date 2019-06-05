'''
Created by Rosa Zhou on 2019/05/07.
Takes in a paragraph-question pair, and outputs a span of consecutive sentences
in the paragraph.
'''
import collections
import load_data
import math
import nltk
from allennlp.predictors.predictor import Predictor

global _TOKENIZER
_TOKENIZER = nltk.tokenize.casual.TweetTokenizer(
    preserve_case=False)

def tokenize(string):
    '''Given a string, consisting of potentially many sentences, returns
    a lower-cased, tokenized version of that string.
    '''
    global _TOKENIZER
    return _TOKENIZER.tokenize(string)

def predictor():
    predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/elmo-constituency-parser-2018.03.14.tar.gz")
    return predictor

def findNP(root, parsedNP):
    if root['nodeType'] == 'NP':
        parsedNP.append(root['word'])
    if 'children' in root.keys():
        for c in root['children']:
            findNP(c, parsedNP)

# def get_all_spans(words):
#     '''
#     returns a list of trigrams in the paragraph, because the average answer
#     length is 3.
#     '''
#     spans = []
#     for i in range(len(words)):
#         #if i+3 < len(words):
#             #spans.append(words[i]+" "+words[i+1]+" "+words[i+2])
#         spans.append(words[i])
#     return spans

def get_unigram_overlap(answer, question):
    '''
    find the overlaped unigrams
    '''
    answer_bag = set(tokenize(answer))
    question_bag = set(tokenize(question))
    overlap = answer_bag.intersection(question_bag)
    return len(overlap)

def get_unigram_counts(doc):
    tlist = tokenize(doc)
    counts = collections.defaultdict(lambda: 0)
    for token in tlist:
        counts[token] += 1
    return counts

def slide_window(answer, question, paragraph):
    '''
    take in 3 strings
    '''
    answer_bag = set(tokenize(answer))
    question_bag = set(tokenize(question))
    S = answer_bag.union(question_bag)
    paragraph_tlist = tokenize(paragraph)
    paragraph_unigram_counts = get_unigram_counts(paragraph)
    max_score = -float("inf")
    for i in range(len(paragraph_tlist)):
        score = 0
        for j in range(len(S)):
            k = i+j
            if k < len(paragraph_tlist):
                word = paragraph_tlist[k]
                score += math.log(1+1/paragraph_unigram_counts[word]) if word in S else 0
        max_score = max(max_score, score)
    return max_score

def get_answer(predictor, paragraph, question):
    '''
    take in 2 strings
    '''
    # get NP in paragraph
    p = predictor.predict(sentence=paragraph)
    root = p['hierplane_tree']['root']
    parsedNP = []
    findNP(root, parsedNP)

    # words = paragraph.split(" ")
    # possible_answers = get_all_spans(words, parsedNP)
    unigram_overlap = {} #alternatively, bigram
    for answer in parsedNP:
        unigram_overlap[answer] = get_unigram_overlap(answer, question)
    #pick max several answers
    #num_candidates = 1 + len(unigram_overlap)//10
    #candidates = sorted(unigram_overlap, key=unigram_overlap.get, reverse=True)[:num_candidates]
    candidates = sorted(unigram_overlap, key=unigram_overlap.get, reverse=True)
    answer = ""
    max_score = -float("inf")
    for candidate_answer in candidates:
        candidate_score = slide_window(candidate_answer, question, paragraph)
        if candidate_score > max_score:
            answer = candidate_answer
            max_score = candidate_score
    return answer
