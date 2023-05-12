# usage:
#
# bert.make_model() retrieves data from DB, makes bert model, writes model to bert_model.csv; usually used after DB update
#
# bert.recommend(book_id)
#   input: book_id
#   return: a list of 12 `book_id`s


from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re
import numpy as np
import nltk
import json
# nltk.download('punkt')


class BookRecommender:

    def __init__(self, filename, columns, t_column, d_column):
        self.filename = filename
        self.columns = columns
        self.title_column = t_column
        self.description_column = d_column
        self.df = None

    def process(self, show=True):
        client = MongoClient(
            'mongodb+srv://group48:gkd48@librarycluster.immrf6e.mongodb.net/')
        collection = client['LibraryDB']
        library_db = collection['db_final']
        data = library_db.find(
            {}, {"_id": 0, 'book_id': 1, 'book_title': 1, 'book_description': 1})
        data = list(data)

        client.close()
        self.df = pd.DataFrame(data)

        # self.df = pd.read_json(self.filename)
        self.df = self.df[self.columns]
        self.df[self.description_column].fillna('', inplace=True)
        self.df[self.description_column] = self.df[self.title_column] + \
            '. ' + self.df[self.description_column].map(str)
        self.df.dropna(inplace=True)
        self.df.drop_duplicates(inplace=True)
        return self.df

    def show_df_records(self, n=5):
        return self.df.head(n)

    def show_info_details(self):
        return self.df.info()

    def __normalize(self, d):
        stopwords = nltk.corpus.stopwords.words('english')
        d = re.sub(r'[^a-zA-Z0-9\s]', '', d, re.I | re.A)
        d = d.lower().strip()
        tks = nltk.word_tokenize(d)
        f_tks = [t for t in tks if t not in stopwords]
        return ' '.join(f_tks)

    def get_normalized_corpus(self, tokens=False):
        n_corpus = np.vectorize(self.__normalize)
        if tokens == True:
            norm_courpus = n_corpus(list(self.df[self.description_column]))
            return np.array([nltk.word_tokenize(d) for d in norm_corpus])
        else:
            return n_corpus(list(self.df[self.description_column]))

    def get_features(self, norm_corpus):
        tf_idf = TfidfVectorizer(ngram_range=(1, 2), min_df=2)
        tfidf_array = tf_idf.fit_transform(norm_corpus)
        return tfidf_array

    def get_vector_cosine(self, tfidf_array):
        return pd.DataFrame(cosine_similarity(tfidf_array))

    def get_bert_weights(self, corpus):
        # https://huggingface.co/sentence-transformers/bert-base-nli-mean-tokens
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        vectors = model.encode(corpus)
        weights = pd.DataFrame(cosine_similarity(vectors))

        return weights

    def search_books_by_term(self, term='book'):
        books = self.df[self.title_column].values
        possible_options = [(i, book) for i, book in enumerate(
            books) for word in book.split(' ') if word == term]
        return possible_options

    def recommendation(self, index, vector, n):
        similarities = vector.iloc[index].values
        similar_indices = np.argsort(-similarities)[1:n + 1]
        books = self.df[self.title_column].values
        similar_books = books[similar_indices]
        return similar_books


mr = None
df = None
norm_corpus = None
wts_df = None


def make_model():
    global mr
    global df
    global norm_corpus
    global wts_df
    mr = BookRecommender('book_collection.json', [
        'book_id', 'book_title', 'book_description'], 'book_title', 'book_description')
    df = mr.process()
    norm_corpus = mr.get_normalized_corpus()
    wts_df = mr.get_bert_weights(norm_corpus)

    wts_df.to_csv('bert_model.csv', index=False)


def recommend(book_id):
    mr = BookRecommender('book_collection.json', [
        'book_id', 'book_title', 'book_description'], 'book_title', 'book_description')
    df = mr.process()

    book_id_index = df['book_id'].to_list()
    wts_df = pd.read_csv("bert_model.csv")

    # books_recommended = mr.recommendation(book_id, wts_df, 12)
    books_recommended = mr.recommendation(book_id_index.index(str(book_id)), wts_df, 8)
    recommendation_list = []
    for title in books_recommended:
        recommendation_list.append(df[df['book_title'] == title].values[0][0])
    return recommendation_list


# def create_book_id_idx():
#     book_id_index = []
    
#     mr = BookRecommender('book_collection.json', [
#         'book_id', 'book_title', 'book_description'], 'book_title', 'book_description')
#     df = mr.process()

#     # for i in range(len(df)):
#     #     book_id_index[i] = df[]

#     book_id_index = df['book_id'].to_list()
#     print(book_id_index)
#     print(type(book_id_index))
#     print(book_id_index[0])



#     # with open("bert_book_idx.json", "w") as outfile:
#     #     json.dump(book_id_index, outfile)
