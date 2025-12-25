import sqlite3
import survey

def query_model(context: str):
    
    trigram_connection = sqlite3.connect(f'./models/n_gram/wikipedia_trigram.db')
    trigram_cursor = trigram_connection.cursor()
    bigram_connection = sqlite3.connect(f'./models/n_gram/wikipedia_bigram.db')
    bigram_cursor = trigram_connection.cursor()

    context_words = context.split(' ')
    response = trigram_cursor.execute(f'''
        SELECT prediction
        FROM n_grams
        WHERE gram = '{context_words[-2] + ' ' + context_words[-1]}'
    ''')

    if response is None:
        response = bigram_cursor.execute(f'''
            SELECT prediction
            FROM n_grams
            WHERE gram = '{context_words[-2] + ' ' + context_words[-1]}'
        ''')
    result = response.fetchall()
    print('Reponse: ' + result[0][0])
    return result[0][0]


def main():
    context = survey.routines.input('Start the sentence: ')
    query_model(context)

if __name__ == '__main__':
    main()
