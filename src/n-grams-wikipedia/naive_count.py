from collections import defaultdict



def print_significant_words(word_counts: dict):
    for word, count in word_counts.items():
        if count > 1000000:
            print(f'word: {word} count: {count}')

word_counts = defaultdict(int)

total_words = 0

with open("./enwiki-latest-pages-articles.xml") as corpus:
    for line in corpus:
        # naive word splitting
        for word in line.split(' '):
            word_counts[word] += 1
            if total_words % 10000000 == 0:
                print(total_words)
                print(print_significant_words(word_counts))
            total_words += 1
