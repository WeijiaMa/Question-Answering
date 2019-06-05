# Question-Answering

## Introduction
This repository implements 3 models: a random guess baseline, a sliding window model, and calls the BIDAF model from the allennlp api. The models are evaluated using EM and F1 scores on the dev set of SQuAD 1.0.

## Run Instruction

### Dataset
The original dataset can be obtained from https://github.com/rajpurkar/SQuAD-explorer/tree/master/dataset.

We have already included the training and dev set in the repository so there is no need to download again.

To obtain the basic dataset statistics, run `python3 load_data.py`, with optional arguments: `--dev_set` and `--training_set` being the path of the dev and training set respectively. By default, they are the SQuad 1.0 datasets.

### Evaluate
First install anaconda. Remember to export the path:

`export PATH=<path-to-anaconda>/bin:$PATH`

Then create a virtural environment and install the dependency of our code.

```shell
conda create -n qa python=3.6
source activate qa
pip install allennlp --upgrade
allennlp
```

The run `python3 evaluate.py` with the `--dev_set` optional arguments as the path to the dev set.

This will print out the up-to-date evaluation metrics (EM and F1) for all 3 models every 10 paragraph in the dev set. By default, this is the SQuAD 1.0 dev set.

## File Description
*load_data.py* provides a method to load the SQuAD json dataset into format our models need.

*baseline1.py* implements the random guess baseline, which returns a unigram.

*baseline2.py* implements the sliding window model as a slightly-better-than-baseline model.

*api.py* is a wrapper of the Machine Comprehension API provided by AllenNLP.

*evaluate.py* implements the metrics and evaluates the 3 models on the dev set.
