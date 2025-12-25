import os
import json
import sqlite3
from tqdm import tqdm

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

def build_model_files(model_name: str, model_counts: dict):
    if not os.path.exists('./models'):
        os.mkdir('./models')
    if not os.path.exists('./models/n_gram'):
        os.mkdir('./models/n_gram')
    if not os.path.exists(f'./models/n_gram/{model_name}'):
        os.mkdir(f'./models/n_gram/{model_name}')

    connection = sqlite3.connect(f'./models/n_gram/{model_name}.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS n_grams(gram, prediction, UNIQUE(gram))')

    print('writing model to disk')
    for n_gram, prediction in tqdm(model_counts.items()):
        print(f"INSERT OR IGNORE INTO n_grams(gram, prediction) VALUES ('{n_gram}', '{prediction[0]}')")
        cursor.execute(f'''INSERT OR IGNORE INTO n_grams(gram, prediction) VALUES (
                       '{n_gram.replace("'", "''")}', '{prediction[0].replace("'", "''")}')''')
    print('model created')
    connection.commit()



def iterate_bigrams():
    bigram_model = {}

    bigram_model = build_model_dictionary("./bigrams.json")
    trigram_model = build_model_dictionary("./trigrams.json")

    print(json.dumps(bigram_model['United'], indent=2))
    print(json.dumps(trigram_model['United States'], indent=2))
    print(json.dumps(trigram_model['Barack Hussein'], indent=2))
    print(json.dumps(trigram_model['States of'], indent=2))

    build_model_files(f'wikipedia_bigram', bigram_model)
    build_model_files(f'wikipedia_trigram', trigram_model)


def main():
    iterate_bigrams()

if __name__ == '__main__':
    main()
