import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import { App } from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter } from 'react-router-dom';
import { action, configure, makeObservable, observable } from "mobx";
import { MCQStore } from "./pages/MedusaMCQ";
import { Observer } from 'mobx-react';

//TODO https://styled-components.com/docs/advanced#theming
// Add themes?
// https://github.com/styled-components/styled-theming


configure({
  enforceActions: "always",
  computedRequiresReaction: true,
  reactionRequiresObservable: true,
  observableRequiresReaction: true,
  disableErrorBoundaries: true
})

// Root Store Declaration
export class RootStore {
  mcqStore!: MCQStore;

  constructor() {
    makeObservable(this, {
      mcqStore: observable,
      addMCQStore: action,
    })
    // this.authStore = new AuthStore(this);
    this.addMCQStore(new MCQStore(this))
  }

  addMCQStore = (store: MCQStore) => {
    this.mcqStore = store;

  }
}

const rootStore = new RootStore()

ReactDOM.render(
  <React.StrictMode>
    <Observer>{() =>
      <BrowserRouter>
        <App store={rootStore}/>
      </BrowserRouter>}
    </Observer>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
