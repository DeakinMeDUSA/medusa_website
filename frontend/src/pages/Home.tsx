import React from "react";
import { observer } from "mobx-react";
import { RootStore } from "../index";
import InstagramFeed from "../js/InstagramFeed"
import { action, makeObservable, observable } from "mobx";
import { JuicerFeed } from "../components/JuicerFeed";
import styled from "styled-components";


class InstaComp {
  myRef: any
  instadata: any;
  store: RootStore
  instafeed: any;
  instahtml: string;

  constructor(store: RootStore) {
    // super(store)

    makeObservable(this, {
      myRef: observable,
      instahtml: observable,
      instafeed: observable,

      dataCallback: action,
      getInstahtml: observable,

    })
    this.store = store;
    this.myRef = React.createRef();
    console.log(this.myRef)
    this.instahtml = ""
    this.instafeed = new InstagramFeed({
      'username': 'medusa.deakin',
      // @ts-ignore
      'container': null,
      'display_profile': true,
      'display_biography': true,
      'display_gallery': true,
      'display_captions': true,
      'callback': this.dataCallback,
      'styling': true,
      'items': 8,
      'items_per_row': 4,
      'margin': 1,
      'lazy_load': true,
      'on_error': console.error
    })
  }

  dataCallback(instadata: any, instahtml: string) {
    console.log(instadata)
    console.log(instahtml)
    this.instadata = instadata
    this.instahtml = `<div>${instahtml}<div>`
  }

  getInstahtml(): string {
    return this.instahtml
  }

}

const JuicerDiv = styled.div`
  width: 75%;
  margin-left: auto;
  margin-right: auto;
  display: block;
`


export const Home = observer(({ store }: { store: RootStore }) => {
  return (
    <div>This is the Home page
      <JuicerDiv><JuicerFeed feedId="medusa-deakin" /></JuicerDiv>
      <div>API Root URL : {store.mcqStore.api.rootURL}</div>
    </div>
    //  TODO use https://instafeedjs.com/#/?id=instafeedjs
  );
})
