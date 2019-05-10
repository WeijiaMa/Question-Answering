'''
Simple baseline model for question answering
Given a question and context, uses random guessing to output a potential answer 
TODO: tokenization step with api tokenizer
Should the potential answers be sentences, phrases, or words? (or all three?)
'''

import load_data
import random

from random import randint



def create_answer(topic, question, paragraphs):
    #should question be irrelevant, or should we make the guessing slightly smarter?
    current_paragraph = paragraphs[topic]
    
    sentences = current_paragraph.split(".")
    # ^ currently the split splits more than sentences
    index = random.randint(0, len(sentences) - 2)
    
    return sentences[index]
    

def main():
    paragraphs, qapairs = load_data.load_data()
    
    for topic in paragraphs:
        for question in qapairs[topic]:           
            answer = create_answer(topic, question, paragraphs)
            print("Q: ", question)
            print("A: ", answer)
    
        
if __name__ == '__main__':
    main()
