import pandas
from pymongo import MongoClient
from rank_bm25 import *
import nltk
from nltk.corpus import stopwords

import re


def bm25_book(book_id):
    nltk_data_path = "nltk"
    if nltk_data_path not in nltk.data.path:
        nltk.data.path.append(nltk_data_path)

    client = MongoClient('mongodb+srv://group48:gkd48@librarycluster.immrf6e.mongodb.net/')
    collection = client['LibraryDB']
    library_db = collection['db_final']
    data = library_db.find({}, {"_id": 0, 'book_id': 1, 'book_title': 1, 'book_description': 1})
    data = list(data)

    client.close()

    book_data_pd = pandas.DataFrame(data)
    stop_words = set(stopwords.words('english'))
    pattern = r"[0-9a-zA-Z\ -']+"
    book_data_pd['tokenized'] = book_data_pd['book_description'].apply(lambda x:  "".join(re.findall(pattern, x.lower())))
    # selected_movie = movie_sim_pd.loc[movie_sim_pd['movie_title'] == ""]
    selected_book = book_data_pd.loc[book_data_pd['book_id'] == str(book_id)]
    selected_token_list = selected_book.tokenized.values[0].split(' ')
    for w in selected_token_list:
        if w in stop_words:
            selected_token_list.remove(w)

    model_tokens_list = book_data_pd.tokenized.values.tolist()
    for i, token in enumerate(model_tokens_list):
        raw_sentence = token.split(' ')
        filtered_sentence = []
        for w in raw_sentence:
            if w not in stop_words:
                filtered_sentence.append(w)
        model_tokens_list[i] = filtered_sentence

    bm25 = BM25Okapi(model_tokens_list)
    book_data_pd['Similarity Score'] = bm25.get_scores(selected_token_list)
    top_20 = bm25.get_top_n(selected_token_list, book_data_pd['book_description'], n=16)
    df_final = book_data_pd[book_data_pd['book_description'].isin(top_20)]
    df_final = df_final.sort_values(by='Similarity Score', ascending=False)
    # print(df_final['book_title'])
    return df_final.loc[df_final.index, 'book_id'].values.tolist()


if __name__ == '__main__':
    print(bm25_book("2"))
