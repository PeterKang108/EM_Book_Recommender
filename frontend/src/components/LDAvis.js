import React from 'react';
import BrNavBar from "./styledComponents/brNavBar";
import styled from 'styled-components';
import Container from "react-bootstrap/Container";

const BRiframe = styled.iframe`
    position: center;
`

const VisDiv = styled(Container)`
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
`


function LDAVisualization() {
    return (
        <div>
            <BrNavBar/>
            <br/>
            <h1>LDA Visualization</h1>
            <br/>
            <VisDiv>
                <BRiframe
                    title="LDA Visualization"
                    src="http://66.42.113.98/api/ldaVis"
                    width="100%"
                    height="860"
                ></BRiframe>
            </VisDiv>
        </div>
    );
}

export default LDAVisualization;