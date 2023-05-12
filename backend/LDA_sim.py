import csv
import re
import pandas
from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
from plsa.algorithms import PLSA
from plsa import Corpus, Pipeline
from plsa.pipeline import DEFAULT_PIPELINE
from scipy.stats import entropy


def jensen_shannon_divergence(p, q):
    p = np.asarray(p)
    q = np.asarray(q)
    m = 0.5 * (p + q)
    return 0.5 * (entropy(p, m) + entropy(q, m))


def find_similar_books_jsd(book_id, top_n=20):
    client = MongoClient('mongodb+srv://group48:gkd48@librarycluster.immrf6e.mongodb.net/')
    collection = client['LibraryDB']
    library_db = collection['db_final']
    data = library_db.find({}, {"_id": 0, 'book_id': 1, 'book_title': 1, 'book_description': 1})
    data = list(data)
    client.close()

    book_df = pd.DataFrame(data)


    # Read the LDA data from train_model.csv
    with open('train_model_final.csv', 'r') as f:
        reader = csv.reader(f)
        lda_rows = [list(map(float, row)) for row in reader]

    input_book_index = book_df[book_df['book_id'] == book_id].index[0]
    input_book_lda = lda_rows[input_book_index]

    # Compute the JSD between the input book and all other books
    js_divergences = [jensen_shannon_divergence(input_book_lda, book_lda) for book_lda in lda_rows]

    # Find the indices of the top_n most similar books
    top_n_indices = np.argsort(js_divergences)[:top_n + 1]

    # Exclude the input book from the results
    top_n_indices = [idx for idx in top_n_indices if idx != input_book_index][:top_n]

    # Get the book_ids and titles of the top_n most similar books
    similar_books = book_df.iloc[top_n_indices][['book_id', 'book_title']]

    return similar_books




def find_similar_books(book_id, top_n=20):
    client = MongoClient('mongodb+srv://group48:gkd48@librarycluster.immrf6e.mongodb.net/')
    collection = client['LibraryDB']
    library_db = collection['db_test4']
    data = library_db.find({}, {"_id": 0, 'book_id': 1, 'book_title': 1, 'book_description': 1})
    data = list(data)
    client.close()

    book_df = pd.DataFrame(data)


    # Read the LDA data from train_model.csv
    with open('train_model4.csv', 'r') as f:
        reader = csv.reader(f)
        lda_rows = [list(map(float, row)) for row in reader]

    input_book_index = book_df[book_df['book_id'] == book_id].index[0]

    # Compute the similarity between the input book and all other books
    similarities = cosine_similarity([lda_rows[input_book_index]], lda_rows)[0]

    # Find the indices of the top_n most similar books
    top_n_indices = np.argsort(similarities)[-top_n - 1:-1][::-1]

    # Get the book_ids and titles of the top_n most similar books
    similar_books = book_df.iloc[top_n_indices][['book_id', 'book_title']]

    return similar_books


def lda_sim(book_id):
    f = open("train_model4.csv", 'r')
    new_result = []
    for line in f:
        row1 = []
        if len(line) == 1:
            continue
        else:
            for num in line.strip().split(','):
                if num == "":
                    continue
                row1.append(float(num))
        new_result.append(row1)
    f.close()

    plsa_result = np.array(new_result)
    client = MongoClient('mongodb+srv://group48:gkd48@librarycluster.immrf6e.mongodb.net/')
    collection = client['LibraryDB']
    library_db = collection['db_test4']
    data = library_db.find({}, {"_id": 0, 'book_id': 1, 'book_title': 1, 'book_description': 1})
    book_data = list(data)

    client.close()

    book_df = pandas.DataFrame(book_data)
    pattern = r"[0-9a-zA-Z\ -']+"
    stop_words = set(stopwords.words('english'))
    tokens = book_df['book_description'].apply(lambda x: "".join(re.findall(pattern, x.lower())))
    new_tokens = []
    index = []
    for i, token in enumerate(tokens):
        words = token.split()
        stemmedlst = [word for word in words if not word in stop_words]
        new_tokens.append(' '.join(stemmedlst))
        index.append(i)
    book_df['tokenized'] = new_tokens
    book_df['index'] = index
    score_dict = {}
    target_movie = plsa_result[book_df[book_df['book_id'] == book_id]['index'].values[0]]
    for i, m in enumerate(plsa_result):
        value = np.sum(target_movie * m)
        if value > 0:
            mov = book_df[book_df['index'] == i]['book_id'].values[0]

            score_dict[mov] = value
    top_20_tuple = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)[1:13]
    top_20 = []
    for t in top_20_tuple:
        top_20.append(t[0])
    print(top_20)
    return top_20


# Example usage:
input_book_id = '2'
similar_books_jsd = find_similar_books_jsd(input_book_id)
# similar_books_cos = find_similar_books(input_book_id)
# similar_books_plsa = lda_sim(input_book_id)
print(similar_books_jsd)
# print(similar_books_cos)
# print(similar_books_plsa)
