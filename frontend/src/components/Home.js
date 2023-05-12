import React, {Fragment, useEffect, useState} from 'react';
import BrNavBar from "./styledComponents/brNavBar";
import Container from "react-bootstrap/Container";
import Card from "react-bootstrap/Card";
import Badge from "react-bootstrap/Badge";
import styled from "styled-components";
import Button from "react-bootstrap/Button";
import Form from 'react-bootstrap/Form';
import {getMovieByID, getRecoVecPlot} from "../utils/api";
import Spinner from "react-bootstrap/Spinner";
import {useNavigate} from "react-router";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";


const MRHomwContainer = styled(Container)`
  margin-top: 50px;
  margin-bottom: 50px;
`

const MRHomeCard = styled(Card)`
  padding: 15px;
  display: flex;
  justify-content: space-around;
  
`

const MRHomeCardButton = styled(Button)`
  max-width: 240px;
  margin-top: 20px;
  margin-bottom: 60px;
  //margin-left: 50%;
  //transform: translate(-50%, 0)

`
const MRForm = styled(Form)`
  
`

const MRdetailCardTitle = styled(Card.Text)`
  margin-top: 15px;
  margin-bottom: 15px;
  font-size: xx-large;
`

const MRFormControl = styled(Form.Control)`
  height: 420px;
  width: 40vw;
`

const MRrecoResultContainerBM25 = styled(Container)`
  margin-bottom: 60px;
  width: 80vw;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-content: center;
`

const MRrecoResultContainer = styled(Container)`
  margin-top: 50px;
  margin-bottom: 50px;
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


const BRSelect = styled(Form.Select)`
  width: 80px;
  height: 40px;
  margin-top: 20px;
  margin-left: 50%;
  transform: translate(-50%, 0);
`

const BRFormText = styled(Form.Text)`
  height: 40px;
  margin-top: 20px;
  padding-right: 0;
`


export default function Home() {
    const nTopicsRange = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17 ,18, 19, 20, 21, 22, 23, 24, 25]
    const navigate = useNavigate()
    const [plot, setPlot] = useState("");
    const [VecData, setVecData] = useState([]);
    const [pressedReco, setPressedReco] = useState(false);
    const [nTopics, setNTopics] = useState(15);
    const [loadingVec, setLoadingVec] = useState(false);

    useState(() => {
        setPlot(" ")
    })

    function onInput({target: {value}}) {
        setPlot(value)
    }

    function fsetNTopics(event) {
        setNTopics(event.target.value)
    }


    function getReco() {
        setPressedReco(true)
        setLoadingVec(true)
        getRecoVecPlot(plot, nTopics).then(res => {
            // console.log(res.data)
            setVecData(res.data)
            setLoadingVec(false)
        })
    }

    function toDetail(book_id) {
        navigate(`/detail/${book_id}`)
        window.location.reload()
    }

    return (
        <div>
            <BrNavBar/>
            <MRHomwContainer>
                <MRHomeCard>
                    <MRForm>
                        <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                            <MRdetailCardTitle>Enter a description of a book to search for similar books in our Database</MRdetailCardTitle>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
                            <MRFormControl
                                as="textarea"
                                rows={5}
                                value={plot}
                                onChange={onInput}
                                placeholder="Enter plot" />
                        </Form.Group>
                        <BRFormText>
                            Set number of results for word2vector space generation
                        </BRFormText>
                        <BRSelect
                            aria-label="Default select example"
                            onChange={fsetNTopics}
                            value={nTopics}
                        >
                            {nTopicsRange.map(n => (
                                    <option value={n}>{n}</option>
                                )
                            )}
                        </BRSelect>
                        <MRHomeCardButton variant="success" onClick={getReco}>Get Recommendation</MRHomeCardButton>
                    </MRForm>
                </MRHomeCard>
            </MRHomwContainer>

            {pressedReco &&
                (<MRrecoResultContainer>
                    <h3>Recommendations By Word2Vec</h3>
                    <hr/>
                    {loadingVec ?
                        (<Spinner animation="border" />) :
                        (<MRrecoResultContainerBM25>

                            {VecData.map(bookData => (
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