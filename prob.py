import math
from nltk.lm import MLE
from nltk.tokenize import word_tokenize

def prepare_tokens(text: str, model: MLE) -> list[str]:
    """
    Tokenize and map OOV words to <UNK> if your model's vocab uses it.
    """
    toks = word_tokenize(text)
    mapped = []
    for t in toks:
        if t in model.vocab:
            mapped.append(t)
        else:
            # if your vocab doesn't contain <UNK>, leaving as-is will make MLE prob 0
            mapped.append('<UNK>' if '<UNK>' in model.vocab else t)
    return mapped

def sentence_logprob(model: MLE, n: int, text: str) -> float:
    """
    Log-probability (natural log) of a sentence under the n-gram model.
    Pads with (n-1) <s> at start and a single </s> at end.
    Returns -inf if any step has zero probability (typical for MLE + unseen n-grams).
    """
    tokens = prepare_tokens(text, model)
    history = ['<s>'] * (n - 1)
    logp = 0.0

    for tok in tokens + ['</s>']:
        context = history[-(n - 1):] if n > 1 else []
        p = model.score(tok, context)
        if p == 0.0:
            return float('-inf')
        logp += math.log(p)
        history.append(tok)

    return logp

def sentence_probability(model: MLE, n: int, text: str) -> float:
    """
    Probability of the full sentence. May underflow for long sentences; use logprob if so.
    """
    lp = sentence_logprob(model, n, text)
    return 0.0 if math.isinf(lp) else math.exp(lp)

def sentence_avg_logprob(model: MLE, n: int, text: str) -> float:
    """
    Average log-probability per token (incl. </s>), natural log.
    """
    tokens = prepare_tokens(text, model)
    lp = sentence_logprob(model, n, text)
    length = len(tokens) + 1  # include </s>
    return float('-inf') if math.isinf(lp) else lp / length

def sentence_perplexity(model: MLE, n: int, text: str) -> float:
    """
    Per-token perplexity using natural logs: exp(-avg_logprob).
    (Close to nltk.lm's perplexity if you pad similarly.)
    """
    avg_lp = sentence_avg_logprob(model, n, text)
    return float('inf') if math.isinf(avg_lp) else math.exp(-avg_lp)
