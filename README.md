# BiGram
$$Project Class 25-26 • Week 1

## Quick Demo
You can run this n-Gram model (and provide feedback!) in my Telegram bot: [@dfg_bigram_project_bot](https://t.me/dfg_bigram_project_bot)
([Backend](https://github.com/LessVegetables/BiGram/tree/main-rbpi) of the bot.)

## Setup
<details>
  <summary>Optional best practice</summary>

### Setup a virtual environment
**Linux/macOS:**
```sh
python -m venv venv
source venv/bin/activate
```

**Windows:**
```sh
python -m venv venv
venv\Scripts\activate
```

</details>

### Running with the "preinstalled" corpa
If you wish to use the pre-prepped [Friends corpus](https://zissou.infosci.cornell.edu/convokit/datasets/friends-corpus/), you may simply run `generate.py`:

```sh
pip install -r requirements.txt
python generate.py
```

### Using your own corpus
To train with your own data:
1. Open `train.py`
2. Change the value of `file_with_train_data` to your file’s path (the code expects data in the same format as `utterances.jsonl`)


## Improvements
Add support for using different/custom corpa from different formats and structures.
Automatic corpus preprocessing.


## Acknowledgements
Special thanks to **Cornell University** and the **ConvoKit** team for providing the Friends Corpus, which this project uses for training and evaluation.s
https://zissou.infosci.cornell.edu/convokit/