''' loads data from dev-v1.1.json file in same directory

makes 2 dictionaries: one where the topics are the keys and the paragraphs
are the values (context_paragraph), the second one the topics are keys and questions/answers are
a tuple (question_dict)
'''
import json

def load_data(file):
    f = json.load(open(file))
    data = f["data"]
    paragraph_list = []
    #paragraph_list stores paragraphs in order
    question_ans_list = []
    #question_ans_list stores a list of qa pair,
    #where each qa pair matches a question to its corresponding list of possible answers
    print("topics",len(data))
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
    dev_para, dev_qa_list = load_data('dev-v1.1.json')
    print("# para in dev: {}".format(len(dev_para)))
    num_qn = sum([len(qa) for qa in dev_qa_list])
    print("# qn in dev: {}".format(num_qn))
    num_ans = sum([sum([len(ans) for ans in qa.values()]) for qa in dev_qa_list])
    print("ave # ans to each qn in dev: {}".format(num_ans/num_qn))
    sum_len_ans = sum([sum([sum([len(a.split()) for a in ans]) for ans in qa.values()]) for qa in dev_qa_list])
    print("ave # words in ans in dev: {}".format(sum_len_ans/num_ans))

    train_para, train_qa_list = load_data('train-v1.1.json')
    print(train_qa_list[0])
    print("# para in train: {}".format(len(train_para)))
    num_qn = sum([len(qa) for qa in train_qa_list])
    print("# qn in train: {}".format(num_qn))
    num_ans = sum([sum([len(ans) for ans in qa.values()]) for qa in train_qa_list])
    print("ave # ans to each qn in train: {}".format(num_ans/num_qn))
    sum_len_ans = sum([sum([sum([len(a.split()) for a in ans]) for ans in qa.values()]) for qa in train_qa_list])
    print("ave # words in ans in train: {}".format(sum_len_ans/num_ans))


if __name__ == "__main__":
    main()
