import csv
from pymongo import MongoClient
import pandas as pd
import numpy as np
from scipy.stats import entropy


def jensen_shannon_divergence(p, q):
    p = np.asarray(p)
    q = np.asarray(q)
    m = 0.5 * (p + q)
    return 0.5 * (entropy(p, m) + entropy(q, m))


def find_similar_books_jsd(book_id, top_n=12):
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
    similar_books = book_df.iloc[top_n_indices][['book_id']]
    similar_books_id_list = [b[0] for b in similar_books.values.tolist()]

    return similar_books_id_list
