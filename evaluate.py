import baseline1
import baseline2
import load_data
import api
from tqdm import tqdm

def get_em(pred, truth):
    ''' return the EM score of a list of predicted answers '''
    em = 0
    for i in range(len(truth)):
        for ans in truth[i]:
            if pred[i] == ans:
                em += 1
                break
    return em/len(truth)

def compute_f1(pred, truth):
    ''' compute the f1 score of two bags of words '''
    tp = len(set.intersection(pred, truth))
    precision = tp/len(pred)
    recall = tp/len(truth)
    if precision + recall == 0: return 0
    return (2 * precision * recall) / (precision + recall)


def get_f1(pred, truth):
    ''' return the micro-averaged f1 score of a list of predicted answers '''
    f1 = 0
    for i in range(len(truth)):
        f1 += max([compute_f1(set(pred[i]), set(ans)) for ans in truth[i]])
    return f1/len(truth)

def main():
    paragraph_list, qa_dict_list = load_data.load_data('dev-v1.1.json')
    if len(paragraph_list) != len(qa_dict_list):
        print("Error: mismatch number of paragraphs and number of qa dictionaries")
        return None

    baseline1_pred = []
    baseline2_pred = []
    api_pred = []
    ground_truth = []
    api_predictor = api.predictor()
    baseline2_predictor = baseline2.predictor()

    for i in tqdm(range(len(paragraph_list))):
        paragraph = paragraph_list[i]
        qa_dict = qa_dict_list[i]
        for question in qa_dict.keys():
            ground_truth_ans = qa_dict[question]
            baseline1_ans = baseline1.get_answer(paragraph, question)
            baseline2_ans = baseline2.get_answer(baseline2_predictor, paragraph, question)
            api_ans = api.get_answer(api_predictor,paragraph, question)

            ground_truth.append(ground_truth_ans)
            baseline1_pred.append(baseline1_ans)
            baseline2_pred.append(baseline2_ans)
            api_pred.append(api_ans)
        if i % 10 == 0:
            print("{} paragraphs: ".format(i))
            for pred in [baseline1_pred, baseline2_pred, api_pred]:
                em = get_em(pred, ground_truth)
                f1 = get_f1(pred, ground_truth)
                print("EM: {}, F1:{}".format(em, f1))

    print("Final performance: ")
    for pred in [baseline1_pred, baseline2_pred, api_pred]:
        em = get_em(pred, ground_truth)
        f1 = get_f1(pred, ground_truth)
        print("EM: {}, F1:{}".format(em, f1))


if __name__ == "__main__":
    main()
