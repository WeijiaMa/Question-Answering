'''
Created by Ziyang Gao on 2019/05/07.
Load SQuAD json dataset into 2 lists: one stores the paragraphs, and the other
stores dictionaries mapping questions in a particular paragraph to answers.
It also prints out the statistics of the dev and training sets.
'''
import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev_set',
                        default='dev-v1.1.json',
                        help='path to dev set')
    parser.add_argument('--training_set',
                        default='train-v1.1.json',
                        help='path to training set')
    return parser.parse_args()


def load_data(file):
    f = json.load(open(file))
    data = f["data"]
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

def get_statistics(para, qa_list):
    print("# para: {}".format(len(para)))
    num_qn = sum([len(qa) for qa in qa_list])
    print("# qn: {}".format(num_qn))
    num_ans = sum([sum([len(ans) for ans in qa.values()]) for qa in qa_list])
    print("ave # ans to each qn: {}".format(num_ans/num_qn))
    sum_len_ans = sum([sum([sum([len(a.split()) for a in ans]) for ans in qa.values()]) for qa in qa_list])
    print("ave # words in ans: {}".format(sum_len_ans/num_ans))

def main():
    args = parse_args()
    dev_para, dev_qa_list = load_data(args.dev_set)
    train_para, train_qa_list = load_data(args.training_set)
    print("Statistics for the dev set: ")
    get_statistics(dev_para, dev_qa_list)
    print("Statistics for the training set: ")
    get_statistics(training_para, training_qa_list)

if __name__ == "__main__":
    main()
