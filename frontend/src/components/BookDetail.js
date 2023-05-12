import React,{useState, useEffect} from 'react'
import {useLocation, useNavigate, useParams} from "react-router";
import {getBert, getBookByID, getRecoBM25, getRecoLDA, getRecoVec} from "../utils/api";
import BRNavbar from "./styledComponents/brNavBar";
import Form from 'react-bootstrap/Form';
import Container from "react-bootstrap/Container";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import styled from 'styled-components';
import Card from "react-bootstrap/Card";
import Badge from "react-bootstrap/Badge";
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';

const MRrecoResultContainer = styled(Container)`
  margin-top: 50px;
  margin-bottom: 50px;
`


const MRdetailCard = styled(Card)`
  padding: 15px;
  display: flex;
  justify-content: space-around;
  background-color: cornsilk;
`

const MRdetailCardTitle = styled(Card.Text)`
  margin-top: 15px;
  margin-bottom: 15px;
  font-size: xx-large;
`

const MRdetailCardButton = styled(Button)`
  max-width: 240px;
  height: 40px;
  margin-top: 80px;
  margin-bottom: 10px;
  margin-left: 50%;
  transform: translate(-50%, 0);
`


const MRrecoResultContainerBM25 = styled(Container)`
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




export default function BookDetail() {
    const navigate = useNavigate()
    const location = useLocation()
    const {bookID} = useParams();

    // const nTopicsRange = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17 ,18, 19, 20, 21, 22, 23, 24, 25]


    const [nTopics, setNTopics] = useState(25);
    const [bookData, setBookData] = useState([]);
    const [BM25Data, setBM25Data] = useState([]);
    const [VecData, setVecData] = useState([]);
    const [LDAData, setLDAData] = useState([]);
    const [BERTData, setBERTData] = useState([]);
    const [rawData, setRawData] = useState();
    const [pressedReco, setPressedReco] = useState(false);
    const [loadingBM25, setLoadingBM25] = useState(false);
    const [loadingVec, setLoadingVec] = useState(false);
    const [loadingLDA, setLoadingLDA] = useState(false);
    const [loadingBERT, setLoadingBERT] = useState(false);

    useState(() => {
        getBookByID(bookID).then(res => {
            // console.log(res.data)
            // console.log(res.data[0]["movie_title"])
            setBookData(res.data[0])
            setRawData(res.data[0].book_id)
        })
    })

    useEffect(() => {
        getBookByID(bookID).then(res => {
            // console.log(res.data)
            // console.log(res.data[0]["movie_title"])
            setBookData(res.data[0])
            setRawData(res.data)
        })
    }, [location])

    function getReco() {
        setPressedReco(true)
        setLoadingBM25(true)
        setLoadingVec(true)
        setLoadingLDA(true)
        setLoadingBERT(true)
        getRecoBM25(bookID).then(res => {
            // console.log(res.data)
            setBM25Data(res.data)
            setLoadingBM25(false)
        })
        // getRecoVec(bookID, nTopics).then(res => {
        //     // console.log(res.data)
        //     setVecData(res.data)
        //     setLoadingVec(false)
        // })
        getRecoLDA(bookID).then(res => {
            console.log(res.data)
            setLDAData(res.data)
            setLoadingLDA(false)
        })
        getBert(bookID).then(res => {
            console.log(res.data)
            setBERTData(res.data)
            setLoadingBERT(false)
        })
    }

    function toDetail(movie_id) {
        navigate(`/detail/${movie_id}`)
        window.location.reload()
    }



    return (
        <div>
            <BRNavbar/>
            {rawData && (<MRrecoResultContainer>
                <MRdetailCard>
                    <Container>
                        <Row>
                            <Col xs={4} md={3}>
                                <Card.Img src={bookData.book_cover} />
                            </Col>
                            <Col xs={14} md={9}>
                                <MRdetailCardTitle>{bookData["book_title"]}</MRdetailCardTitle>
                                <Card.Text>{bookData["book_author"]}</Card.Text>
                                <Card.Text>{bookData["book_releaseDate"]} | {bookData["book_releaseDetail"]}</Card.Text>
                                <Card.Text>GoodRead rating: {bookData["book_rating"]}</Card.Text>
                                <hr/>
                                <div dangerouslySetInnerHTML={{ __html: bookData.book_description_raw }} />
                                <hr/>
                                {bookData.book_genre.map(genres => (
                                    <BRBadge bg="secondary">
                                        {genres}
                                    </BRBadge>
                                ))}
                            </Col>
                        </Row>
                        <Row>
                            <MRdetailCardButton variant="success" onClick={getReco}>Get Recommendation</MRdetailCardButton>
                        </Row>
                    </Container>

                </MRdetailCard>
            </MRrecoResultContainer>)}

            {pressedReco &&
                (<MRrecoResultContainer>
                    <h3>Recommendations By BM25 Okapi</h3>
                    <hr/>
                    {loadingBM25 ?
                        (<Spinner animation="border" />) :
                        (<MRrecoResultContainerBM25>
                            {BM25Data.map(bookData => (
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
                                </MRResultCard>))}
                        </MRrecoResultContainerBM25>)}
                </MRrecoResultContainer>)}

            {pressedReco &&
                (<MRrecoResultContainer>
                    <h3>Recommendations By LDA</h3>
                    <hr/>
                    {loadingLDA ?
                        (<Spinner animation="border" />) :
                        (<MRrecoResultContainerBM25>

                            {LDAData.map(bookData => (
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
                                </MRResultCard>))}
                        </MRrecoResultContainerBM25>)}
                </MRrecoResultContainer>)}

            {pressedReco &&
                (<MRrecoResultContainer>
                    <h3>Recommendations By BERT</h3>
                    <hr/>
                    {loadingBERT ?
                        (<Spinner animation="border" />) :
                        (<MRrecoResultContainerBM25>

                            {BERTData.map(bookData => (
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
                                </MRResultCard>))}
                        </MRrecoResultContainerBM25>)}
                </MRrecoResultContainer>)}
        </div>
    )
}