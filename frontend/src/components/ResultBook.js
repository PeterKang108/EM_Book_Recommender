import React, {useEffect, useState} from 'react';
import BRNavBar from "./styledComponents/brNavBar";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import {useNavigate, useParams} from "react-router";
import {getBookByID, searchBookTitle} from "../utils/api";
import Badge from 'react-bootstrap/Badge';
import styled from 'styled-components';

const MRResultContainer = styled(Container)`
  
  //max-width: 1000px;
  margin-top: 40px;
  margin-bottom: 60px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-content: center;
`

const MRResultCard = styled(Card)`
  margin: 15px;
  padding: 5px;
  background-color: cornsilk;
`

const MRResultCardText = styled(Card.Text)`
  font-size: 10pt;
`

const MRResultCardText1 = styled(Card.Text)`
  font-size: 11pt;
  margin-left: 3px;
  margin-right: 3px;
  margin-bottom: 3px;
`

const BRBadge = styled(Badge)`
  margin-left: 5px;
  margin-right: 5px;
`



export default function ResultBook() {
    const navigate = useNavigate()
    const {bookTitle} = useParams();
    const [rawData, setRawData] = useState();
    const [bookDataList, setBookDataList] = useState([]);
    console.log(bookTitle)

    useState(() => {
        searchBookTitle(bookTitle).then(res => {
            console.log(res.data)
            setRawData(res)
            setBookDataList(res.data)
        })
    })

    function toDetail(book_id) {
        navigate(`/detail/${book_id}`)
        window.location.reload()
    }


    return (
        <div>
            <BRNavBar
                bookTitle={bookTitle}
            />
            <MRResultContainer>
                {rawData &&
                    (bookDataList.map(bookData => (
                        <MRResultCard
                            key={bookData.book_id}
                            style={{ width: '18rem' }}
                            onClick={() => toDetail(bookData.book_id)}
                        >
                            <Card.Img variant="top" src={bookData.book_cover} />
                            <Card.Body>
                                <Card.Title>{bookData.book_title}</Card.Title>
                                {bookData.book_author.map(book_author => (
                                    <MRResultCardText1>{book_author}</MRResultCardText1>
                                ))}
                                <MRResultCardText>{bookData.book_releaseDate[0]}</MRResultCardText>
                                {bookData.book_genre.map(genres => (
                                    <BRBadge bg="secondary">
                                            {genres}
                                    </BRBadge>
                                ))}
                                {/*<Button variant="primary">Go somewhere</Button>*/}
                            </Card.Body>
                        </MRResultCard>)))
                }
            </MRResultContainer>
        </div>
    )
}