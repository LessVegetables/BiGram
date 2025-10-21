import os
import json

import nltk
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE, Vocabulary
from pathlib import Path
import pickle

SENTENCE_LENGTH = 10

file_with_train_data = "utterances.jsonl"

tokenized_corpus = [] # must be a list of tokenized sentences

with open(file_with_train_data, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            utterance = json.loads(line)

            for sentence in utterance["meta"]["tokens"]:
                if len(sentence) != 0:
                    tokenized_corpus.append([tkn.lower() for tkn in sentence])

# replace for loop with just "n = 2" for a bigram model
for n in range (1, 5):
    print(f"Training a {n}-gram model...")

    vocab = Vocabulary([w for sent in tokenized_corpus for w in sent], unk_cutoff=2)
    train_data, padded_sents = padded_everygram_pipeline(n, tokenized_corpus) # accepts a list of lists

    model = MLE(n, vocabulary=vocab)
    model.fit(train_data, padded_sents)
    print("Model trained!")

    path = f"chat_{n}_gram.pkl"
    with open(path, 'wb') as f:
        pickle.dump({'order': model.order, 'model': model}, f, protocol=pickle.HIGHEST_PROTOCOL)
