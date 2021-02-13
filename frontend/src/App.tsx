import React from 'react';
import './App.css';
import { Main } from "./components/Main";
import { Navbar } from "./components/Navbar";
import { RootStore } from "./components/RootStore";
import { observer } from "mobx-react";


export const App = observer(({ store }: { store: RootStore }) => {
  return (
    // <Provider
    //   rootStore={rootStore}
    //   mcqStore={rootStore.mcqStore}
    // authStore={rootStore.authStore}
    // >
    <div className="App">
      <Navbar store={store}/>
      <Main store={store}/>
    </div>
    // {/*</Provider>*/}
  )
})
