''' loads data from dev-v1.1.json file in same directory

makes 2 dictionaries: one where the topics are the keys and the paragraphs
are the values (context_paragraph), the second one the topics are keys and questions/answers are
a tuple (question_dict)
'''
import json

def load_data():
    d = json.load(open('dev-v1.1.json'))

    innerfile = d["data"]

    context_paragraph = {}
    #context_paragraph maps each topic to its paragraph

    question_dict = {}
    #question_dict maps each topic to a list of questions


    for i in innerfile:
        subject = i["title"]
        context_paragraph[subject] = i["paragraphs"][0]["context"]
        question_set = i["paragraphs"][0]["qas"]
        question_list = []
        answer_list = []
        for j in question_set:
            question_list.append(j["question"])
            answer_options = []
            for k in j["answers"]:
                answer_options.append(k["text"])
            answer_list.append(answer_options)

        question_dict[subject] = (question_list, answer_list)

    #print(context_paragraph["Super_Bowl_50"])
    #print(question_dict["Super_Bowl_50"])



def main():
    load_data()


if __name__ == "__main__":
    main()
