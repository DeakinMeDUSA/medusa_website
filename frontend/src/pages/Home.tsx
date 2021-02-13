import React from "react";
import { observer } from "mobx-react";
import { RootStore } from "../components/RootStore";
import { JuicerFeed } from "../components/JuicerFeed";
import styled from "styled-components";


const JuicerDiv = styled.div`
  width: 75%;
  margin-left: auto;
  margin-right: auto;
  display: block;
`


export const Home = observer(({ store }: { store: RootStore }) => {
  return (
    <div>This is the Home page
      <JuicerDiv><JuicerFeed feedId="medusa-deakin" maxItems={10}/></JuicerDiv>
      <div>API Root URL : {store.mcqStore.api.rootURL}</div>
    </div>
    //  TODO use https://instafeedjs.com/#/?id=instafeedjs
  );
})
