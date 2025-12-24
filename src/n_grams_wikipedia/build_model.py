from collections import defaultdict
import copy
from datetime import timedelta
import json
import re
import sys
import time
from functools import lru_cache
from tqdm import tqdm

START_TIME = time.perf_counter()

def build_model_dictionary(n_gram_count_file: str) -> dict:
    n_gram_model = {}

    with open(n_gram_count_file) as n_gram_counts:
        print(f'parsing model file: {n_gram_count_file}')
        all_n_grams = json.loads(n_gram_counts.read())
        print('iterating n_grams')
        for n_gram, count in tqdm(all_n_grams.items()):
            split_index = len(n_gram) - 1
            while n_gram[split_index] != ' ':
                split_index -= 1
            if n_gram[0:split_index] not in n_gram_model or count > n_gram_model[n_gram[0:split_index]][1]:
                n_gram_model[n_gram[0:split_index]] = (n_gram[split_index+1:], count) 
    return n_gram_model

def iterate_bigrams():
    bigram_model = {}

    bigram_model = build_model_dictionary("./bigrams.json")
    trigram_model = build_model_dictionary("./trigrams.json")

    print(json.dumps(bigram_model['United'], indent=2))
    print(json.dumps(trigram_model['United States'], indent=2))
    print(json.dumps(trigram_model['Barack Hussein'], indent=2))
    print(json.dumps(trigram_model['States of'], indent=2))

def main():
    iterate_bigrams()

if __name__ == '__main__':
    main()
