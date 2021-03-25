import React from 'react';
import './App.css';
import { RootStore } from "./RootStore";
import { observer } from "mobx-react";
import { QuestionsList } from "./QuestionsList";


const stateRender = (store: RootStore) => {
  if (store.mode === "questions_list") {
    return <QuestionsList store={store}/>
  } else if (store.mode === "answer_questions"){
    return <QuestionsList store={store}/>
  } else if (store.mode === "review_questions"){
    return <QuestionsList store={store}/>
  }
  // if (!store.parseRequest.processing && !store.parseRequest.ready) {
  //     if (!store.optionsScreen) {
  //   return <div>{CVDropzone({ store: store })}</div>;
  //     } else {
  //   return <RedactOptions store={store}/>;
  //     }
  // } else if (!store.parseRequest.ready) {
  //   return <Processing store={store}/>;
  // } else {
  //   return <Completed store={store}/>;
  // }
};

export const App = observer(({ store }: { store: RootStore }) => {
  return (
    // <Provider
    //   rootStore={rootStore}
    //   mcqStore={rootStore.mcqStore}
    // authStore={rootStore.authStore}
    // >
    <div className="App">
      {stateRender(store)}


    </div>
    // {/*</Provider>*/}
  )
})
