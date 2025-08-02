from collections import defaultdict
import copy
from datetime import timedelta
import json
import re
import sys
import time
from functools import lru_cache

START_TIME = time.perf_counter()

def print_significant(counts: dict):
    for item, count in counts.items():
        if count > 10000:
            print(f'gram: ```{' '.join(item)}``` count: {count}')


def log_progress(trigrams, bigrams, total_words):
    if total_words % 1000000 == 0:
        print(f'total_words: {total_words:,}, time: {timedelta(seconds=time.perf_counter()-START_TIME)}s')
        print(f'size of bigrams: {len(bigrams):,} keys, {sys.getsizeof(bigrams) / 1000000000} GB')
        print(f'size of trigrams: {len(trigrams):,} keys, {sys.getsizeof(trigrams) / 1000000000} GB')
    if total_words % 100000000 == 0:
        print(print_significant(trigrams))

def strip_dictionary(grams):
    keys_to_delete = []
    for gram, count in grams.items():
        if count == 1:
            keys_to_delete.append(gram)
    print(f'DELETING KEYS: {len(keys_to_delete)}')
    for key in keys_to_delete:
        del grams[key]
    return grams 

valid_punctuation_cache = {',', '.', '?', '\''}
@lru_cache(maxsize=20000000)
def is_valid_word(word):
    for char in word:
        if not (char.isalnum() or char in valid_punctuation_cache):
             return False
    return True

def iterate_corpus(trigrams, bigrams, total_words):
    with open("./enwiki-latest-pages-articles.xml") as corpus:
        for line_index, line in enumerate(corpus):
            # Naive stripping of the xml tags and the citation elements
            # line = re.sub('<[^>]*>', '', line)
            # line = re.sub('{{.*}}', '', line)
            # line = re.sub(r'\[\[', '', line)
            # line = re.sub(r'\]\]', '', line)
            # line = re.sub(r'\|', '', line)
            # line = re.sub('\n', '', line)
            words = line.split(' ')
            
            for i, word in enumerate(words):
                if len(word) == 0 or not is_valid_word(word):
                    continue
                if i >= 1:
                    if not is_valid_word(words[i-1]):
                        continue
                    bigram = (words[i-1], word)
                    bigrams[bigram] += 1
                if i >= 2:
                    if not is_valid_word(words[i-2]):
                        continue
                    trigram = (words[i-2], words[i-1], word)
                    if trigram in trigrams:
                        trigrams[trigram] += 1
                    else:
                        trigrams[trigram] = 1

                log_progress(trigrams, bigrams, total_words)
                total_words += 1

                if total_words % 20000000 == 0:
                    # We strip insignificant n-grams (occurring only once every 20 million words)
                    # as they eat too much RAM for their value and their probabilities can
                    # be estimated after-the-fact
                    bigrams = strip_dictionary(bigrams)
                    trigrams = strip_dictionary(trigrams)
    return trigrams, bigrams, total_words

def main():
    trigrams = {}
    bigrams = defaultdict(int)
    total_words = 0

    trigrams, bigrams, total_words = iterate_corpus(trigrams,bigrams,total_words)

    pretty_bigrams = {}
    for bigram, count in bigrams.items():
        pretty_bigram = ' '.join(bigram)
        pretty_bigrams[pretty_bigram] = count

    pretty_trigrams = {}
    for trigram, count in trigrams.items():
        pretty_trigram = ' '.join(trigram)
        pretty_trigrams[pretty_trigram] = count

    with open('bigrams.json', 'w') as bigrams_file:
        json.dump(pretty_bigrams, bigrams_file, indent=1)
    with open('trigrams.json', 'w') as trigrams_file:
        json.dump(pretty_trigrams, trigrams_file, indent=1)

if __name__ == '__main__':
    main()
