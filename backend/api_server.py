import os

from fastapi import Request, FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from db_actions import *
from LDA import find_similar_books_jsd
from VEC import vec_book
from BM25 import bm25_book
from bert import recommend


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:80",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    book_id_or_description: str
    n_topics: int


# app.mount("/ldaVis", StaticFiles(directory="/"), name="lda_visualization.html")


@app.get("/api/ldaVis")
async def read_index():
    return FileResponse('lda_visualization.html')


@app.get("/api/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/db_get_by_id/{book_id}")
async def get_book_by_id(book_id: str):
    response = get_by_id(book_id)
    return response


@app.get("/api/db_get_by_title/{book_title}")
async def get_book_by_title(book_title: str):
    response = get_by_title(book_title)
    return response


@app.get("/api/bm25/{book_id}")
async def bm25_compare(book_id: str):
    result_id_list = bm25_book(book_id)
    response = get_by_multiple_id_brief(result_id_list)
    return response


@app.post("/api/vectordb")
async def vector_db(data: Item):
    book_id = data.book_id_or_description
    n_topics = data.n_topics
    result_id_list = vec_book(book_id, n_topics)
    response = get_by_multiple_id_brief(result_id_list)
    return response


@app.post("/api/vectornew")
async def vector_new(data: Item):
    new_des = data.book_id_or_description
    n_topics = data.n_topics
    result_id_list = vec_book(new_des, n_topics)
    response = get_by_multiple_id_brief(result_id_list)
    return response


@app.get("/api/lda/{book_id}")
async def lda_book(book_id: str):
    result_id_list = find_similar_books_jsd(book_id)
    response = get_by_multiple_id_brief(result_id_list)
    return response


@app.get("/api/bert/{book_id}")
async def bert_book(book_id: str):
    result_id_list = recommend(book_id)
    response = get_by_multiple_id_brief(result_id_list)
    return response


# @app.on_event("startup")
# async def connect_to_db():
#     isExist = os.path.exists("train_model_PLSA.csv")
#     if not isExist:
#         plsa_train(10)
#     return


