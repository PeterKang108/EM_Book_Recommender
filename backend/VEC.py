import pandas
from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import re


def vec_book(search_input, n_topics, input_type="words"):
    download_path = "nltk"
    nltk_data_path = download_path
    if nltk_data_path not in nltk.data.path:
        nltk.data.path.append(nltk_data_path)
    client = MongoClient('mongodb+srv://group48:gkd48@librarycluster.immrf6e.mongodb.net/')
    collection = client['LibraryDB']
    library_db = collection['db_final']
    data = library_db.find({}, {"_id": 0, 'book_id': 1, 'book_title': 1, 'book_description': 1})
    book_data = list(data)
    client.close()
    book_df = pandas.DataFrame(book_data)
    pattern = r"[0-9a-zA-Z\ -']+"
    stop_words = set(stopwords.words('english'))
    tokens = book_df['book_description'].apply(lambda x: "".join(re.findall(pattern, x.lower())))
    new_tokens = []
    for token in tokens:
        words = token.split()
        stemmedlst = [word for word in words if not word in stop_words]
        new_tokens.append(' '.join(stemmedlst))
    book_df['tokenized'] = new_tokens
    if input_type == "words":
        selected_movie = "".join(re.findall(pattern, search_input.lower()))
    else:
        selected_movie = book_df.loc[book_df['book_id'] == str(search_input)].tokenized.values[0]
    score_dict = {}
    for i in book_df['book_id']:
        movie = book_df.loc[book_df['book_id'] == str(i)].tokenized.values[0]
        target_vector = [selected_movie, movie]
        vectorizer = CountVectorizer(stop_words='english')
        vectorizer.fit_transform(target_vector)
        a, b = vectorizer.transform([target_vector[0]]), vectorizer.transform([target_vector[1]])
        score = cosine_similarity(a, b)
        score_dict[i] = score[0][0]
    if input_type == "words":
        top_10_tuple = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)[:n_topics]
    else:
        top_10_tuple = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)[1:n_topics + 1]
    top_10 = []
    for t in top_10_tuple:
        top_10.append(t[0])
    return top_10

