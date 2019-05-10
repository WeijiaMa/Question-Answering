''' loads data from dev-v1.1.json file in same directory

makes 2 dictionaries: one where the topics are the keys and the paragraphs
are the values (context_paragraph), the second one the topics are keys and questions/answers are
a tuple (question_dict)
'''
import json

def load_data():
    file = json.load(open('dev-v1.1.json'))
    data = file["data"]
    paragraph_list = []
    #paragraph_list stores paragraphs in order
    question_ans_list = []
    #question_ans_list stores a list of qa pair,
    #where each qa pair matches a question to its corresponding list of possible answers

    for topic in data:
        for paragraph in topic["paragraphs"]:
            paragraph_list.append(paragraph["context"])
            question_set = paragraph["qas"]
            qa_pairs = {}
            for qn in question_set:
                question = qn["question"]
                answer = [ans["text"] for ans in qn["answers"]]
                qa_pairs[question] = answer
            question_ans_list.append(qa_pairs)

    return paragraph_list, question_ans_list

def main():
    load_data()

if __name__ == "__main__":
    main()
