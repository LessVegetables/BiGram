import os
import random

import nltk
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE, Vocabulary
from nltk.tokenize import word_tokenize
from pathlib import Path
import pickle



def load_model(path):
    with open(path, 'rb') as f:
        payload = pickle.load(f)
    return payload['model'], payload['order']


def is_contraction(word) -> bool:
    contractions = ["n\'t", "\'d", "\'s", "\'m", "\'re", "\'ll", "\'ve"]
    for contr in contractions:
        if contr in word:
            return True
    return False


def cleanup_text(message: list) -> str:
    cleaned_message = ''

    # removing duplicate </s>
    seen_s = False
    i = 0
    while i < len(message):
        if message[i] == '</s>':
            if not seen_s:
                seen_s = True
                i += 1
            else:
                message.pop(i)

        else:
            seen_s = False
            i += 1

    for word in message:
        if word not in ['<s>', '<UNK>', '\'', '`']:     

            if word in '.?!,():;«»\"\'':
                if cleaned_message == '':
                    continue
                else:
                    cleaned_message += word
            else:
                if cleaned_message == '':
                    cleaned_message = word.capitalize()
                elif '</s>' in word:
                    if cleaned_message[-1] not in '.?!()':
                        ending = random.choice(".?!")
                        cleaned_message = cleaned_message + ending
                elif cleaned_message[-1] in '.?!' or word == "i":
                    cleaned_message = cleaned_message + ' ' + word.capitalize()
                elif is_contraction(word):
                    cleaned_message = cleaned_message + word
                else:
                    cleaned_message = cleaned_message + ' ' + word
    # говорят это всё можно было заменить на regex фильтр. .........Окей! 🙂
    return cleaned_message


def is_word(tok: str) -> bool:
    return any(ch.isalpha() for ch in tok)


def generate_sentence(model: MLE, n: int, sentence_len: int, max_sentence_len=20, random_seed=None) -> str:

    PUNCT = {'.', '?', '!', ',', '(', ')', ':', ';'}
    SPECIAL = {'<s>', '</s>', '<UNK>'}


    word_count = 0
    history = ['<s>'] * (n-1)

    def sample_token(history):
        # try a few times to avoid infinite loops on filtered tokens
        for _ in range(100):
            tok = model.generate(1, history, random_seed)
            # reject punctuation as first token
            if not (word_count == 0 and tok in '.?!,():;'):
                if tok == '<UNK>':
                    continue
                if tok == '</s>' and word_count < sentence_len:
                    continue
                return tok
        return '<UNK>'  # give up (or NONE)
    
    
    while word_count < max_sentence_len:
        if sentence_len <= word_count:
            # ends "naturaly"?
            if (history[-1][-1] in '.?!();') or (history[-1] == '</s>'):

                break

        token = sample_token(history)
        history.append(token)
        if (token not in PUNCT) and (token not in SPECIAL):
            if is_word(token) and ("\'" not in token):
                word_count += 1

    # print(word_count, ' '.join(history), end='\t———\t')
    message = cleanup_text(history)

    return message

if __name__ == "__main__":

    # ------------------------
    num_lines = 5
    min_len = 10
    max_len = 15
    # ------------------------

    models_path = ["chat_1_gram.pkl",
                   "chat_2_gram.pkl",
                   "chat_3_gram.pkl",
                   "chat_4_gram.pkl"]

    for model_path in models_path:
        model, n = load_model(os.path.join("models", model_path))
        print(f"Loaded {n}-gram model from {model_path}")

        for i in range(num_lines):
            print(f"{i+1}:", generate_sentence(model, n, min_len, max_sentence_len=max_len))
