from allennlp.predictors.predictor import Predictor

def predictor():
    predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/bidaf-model-2017.09.15-charpad.tar.gz")
    return predictor

def get_answer(predictor, paragraph, question):
    p = predictor.predict(passage=paragraph, question=question)
    ans = p["best_span_str"]
    return ans
