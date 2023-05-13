import pandas as pd
from pymongo import MongoClient
import re
import gensim
from gensim import corpora
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
import nltk
import numpy as np
import csv

nltk_data_path = "G:/workspace/cs510/final_project/backend/nltk"
if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)


client = MongoClient('mongodb+srv://group48:gkd48@librarycluster.immrf6e.mongodb.net/')
collection = client['LibraryDB']
library_db = collection['db_final']
data = library_db.find({}, {"_id": 0, 'book_id': 1, 'book_title': 1, 'book_description': 1})
data = list(data)
client.close()

book_df = pd.DataFrame(data)
topic_num = 18

stop_words = nltk.corpus.stopwords.words('english')
texts = [
    [word for word in gensim.utils.simple_preprocess(book_desc.lower()) if word not in stop_words]
    for book_desc in book_df['book_description']
]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lda = gensim.models.ldamodel.LdaModel(corpus, num_topics=topic_num, id2word=dictionary, passes=15)
vis_data = gensimvis.prepare(lda, corpus, dictionary)
pyLDAvis.save_html(vis_data, 'lda_visualization.html')
topics = lda.get_document_topics(corpus)

rows = []
for doc_topics in topics:
    row = []
    for i in range(0, topic_num):
        row.append(0)
    for topic_id, topic_prob in doc_topics:
        row[topic_id] = topic_prob
    rows.append(row)

with open('train_model_final.csv', 'w', newline='') as f:
    write = csv.writer(f)
    write.writerows(rows)
f.close()

print('completed PLSA training')
