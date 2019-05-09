'''
Created by Rosa Zhou on 2019/05/07.
Takes in a paragraph-question pair, and outputs a span of consecutive sentences
in the paragraph.
'''
import collections
import load_data
import math
import nltk

global _TOKENIZER
_TOKENIZER = nltk.tokenize.casual.TweetTokenizer(
    preserve_case=False)

def tokenize(string):
    '''Given a string, consisting of potentially many sentences, returns
    a lower-cased, tokenized version of that string.
    '''
    global _TOKENIZER
    return _TOKENIZER.tokenize(string)

def get_all_spans(sentences):
    spans = []
    for i in range(len(sentences)):
        for j in range(i+1,len(sentences)):
            spans.append(''.join(sentences[i:j]))
    return spans

def get_unigram_overlap(answer, question):
    '''
    find the overlaped unigrams divided by length of answer
    '''
    answer_bag = set(tokenize(answer))
    question_bag = set(tokenize(question))
    overlap = answer_bag.intersection(question_bag)
    return len(overlap)/len(answer)

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

def get_answer(paragraph, question):
    '''
    take in 2 strings
    '''
    sentences = paragraph.split(".")
    possible_answers = get_all_spans(sentences)
    unigram_overlap = {} #alternatively, bigram
    for answer in possible_answers:
        unigram_overlap[answer] = get_unigram_overlap(answer, question)
    #pick max several answers
    num_candidates = 1 + len(unigram_overlap)//10
    candidates = sorted(unigram_overlap, key=unigram_overlap.get, reverse=True)[:num_candidates]
    answer = ""
    max_score = -float("inf")
    for candidate_answer in candidates:
        candidate_score = slide_window(candidate_answer, question, paragraph)
        if candidate_score > max_score:
            answer = candidate_answer
            max_score = candidate_score
    return answer

def main():
    topic_paragraph, topic_qlist = load_data.load_data()
    topics = set(topic_paragraph.keys()).intersection(set(topic_qlist.keys()))
    for topic in topics:
        paragraph = topic_paragraph[topic]
        qlist = topic_qlist[topic]
        for question in qlist:
            print(get_answer(paragraph, question))
            break

if __name__ == "__main__":
    main()
