from pymongo import MongoClient
import re

collection_name = "db_final"


def get_by_id(book_id):
    client = MongoClient('mongodb+srv://group48:gkd48@librarycluster.immrf6e.mongodb.net/')
    collection = client['LibraryDB']
    library_db = collection[collection_name]
    data = library_db.find({'book_id': str(book_id)}, {'_id': 0})
    data = list(data)
    client.close()
    return data


def get_by_title(book_title):
    client = MongoClient('mongodb+srv://group48:gkd48@librarycluster.immrf6e.mongodb.net/')
    collection = client['LibraryDB']
    library_db = collection[collection_name]
    book_title_re = re.compile(str(book_title), re.IGNORECASE)
    data = library_db.find({'book_title': book_title_re}, {'_id': 0, 'book_id': 1, 'book_author': 1, 'book_title': 1,
                                                           'book_cover': 1, 'book_releaseDate': 1,
                                                           'book_releaseDetail': 1,
                                                           'book_genre': 1, 'book_rating': 1})
    data = list(data)
    client.close()
    return data


def get_by_multiple_id_brief(book_id_list):
    client = MongoClient('mongodb+srv://group48:gkd48@librarycluster.immrf6e.mongodb.net/')
    collection = client['LibraryDB']
    library_db = collection[collection_name]
    data = []
    for book_id in book_id_list:
        data += list(
            library_db.find({'book_id': str(book_id)}, {'_id': 0, 'book_id': 1, 'book_author': 1, 'book_title': 1,
                                                        'book_cover': 1, 'book_releaseDate': 1, 'book_releaseDetail': 1,
                                                        'book_genre': 1, 'book_rating': 1}))
    data = list(data)
    client.close()
    return data
