import axios from 'axios'

const BookRecommender = axios.create({
    timeout: 50000,
    // baseURL: 'http://localhost:8000/api'
    baseURL: 'http://66.42.113.98/api'

})

export function getBookByID(book_id) {
    return BookRecommender({
        method: 'GET',
        url: `/db_get_by_id/${book_id}`
    })
}

export function searchBookTitle(book_title) {
    return BookRecommender({
        method: 'GET',
        url: `/db_get_by_title/${book_title}`
    })
}

export function getRecoBM25(book_id) {
    return BookRecommender({
        method: 'GET',
        url: `/bm25/${book_id}`
    })
}

export function getBert(book_id) {
    return BookRecommender({
        method: 'GET',
        url: `/bert/${book_id}`
    })
}


export function getRecoVec(book_id, n_topics) {
    return BookRecommender({
        method: 'POST',
        url: `/vectordb`,
        data: {
            book_id_or_description: book_id,
            n_topics: n_topics
        }
    })
}

export function getRecoVecPlot(book_description, n_topics) {
    return BookRecommender({
        method: 'POST',
        url: `/vectornew`,
        data: {
            book_id_or_description: book_description,
            n_topics: n_topics
        }
    })
}

export function getRecoLDA(book_id) {
    return BookRecommender({
        method: 'GET',
        url: `/lda/${book_id}`
    })
}