import React from 'react';
import './App.css';
import { RootStore } from "./components/RootStore";
import { observer } from "mobx-react";
import { MedusaMCQ } from "./components/MedusaMCQ";


export const App = observer(({ store }: { store: RootStore }) => {
  return (
    // <Provider
    //   rootStore={rootStore}
    //   mcqStore={rootStore.mcqStore}
    // authStore={rootStore.authStore}
    // >
    <div className="App">
      <MedusaMCQ store={store}/>
    </div>
    // {/*</Provider>*/}
  )
})
