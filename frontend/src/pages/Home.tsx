import React from "react";
import { observer } from "mobx-react";
import { RootStore } from "../index";
import InstagramFeed from "../js/InstagramFeed"

@observer
class InstaComp extends React.Component {
  myRef: any
  private instafeed: any;
  instadata: any;
  private instahtml: string;
  store : RootStore

  constructor(store: RootStore) {
    super(store)
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

  dataCallback(instadata: any, instahtml: string){
    console.log(instadata)
    console.log(instahtml)
    this.instadata = instadata
    this.instahtml = instahtml
  }

  render() {
    return (<div>{this.instahtml}</div>)
  }
}


export const Home = observer(({ store }: { store: RootStore }) => {
  return (
    <div>This is the Home page
      <div>API Root URL : {store.mcqStore.api.rootURL}</div>
      <InstaComp/>
    </div>
    //  TODO use https://instafeedjs.com/#/?id=instafeedjs
  );
})

