import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import { App } from './App';
import { configure } from "mobx";
import { RootStore } from "./RootStore";

//TODO https://styled-components.com/docs/advanced#theming
// Add themes?
// https://github.com/styled-components/styled-theming


configure({
  enforceActions: "observed",
  computedRequiresReaction: true,
  reactionRequiresObservable: true,
  observableRequiresReaction: true,
  disableErrorBoundaries: true
})


ReactDOM.render(
  <App store={new RootStore()}/>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
