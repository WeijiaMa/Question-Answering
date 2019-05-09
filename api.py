from allennlp.predictors.predictor import Predictor
import spacy
predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/bidaf-model-2017.09.15-charpad.tar.gz")
p = predictor.predict(
  passage="The Matrix is a 1999 science fiction action film written and directed by The Wachowskis, starring Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving, and Joe Pantoliano.",
  question="Who stars in The Matrix?"
)
ans = p["best_span_str"]
print("Predicted ans: {}".foramt(ans))
print("Done")
