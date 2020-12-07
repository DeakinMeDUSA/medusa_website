import React from 'react';
import { Route, Switch } from 'react-router-dom';

import { Home } from '../pages/Home';
import { MedusaMCQ } from "../pages/MedusaMCQ";
import { RootStore } from "../index";
import { Observer, observer } from "mobx-react";

export const Main = observer(({ store }: { store: RootStore }) => {
  return <Observer>{() =>
    <Switch> {/* The Switch decides which component to show based on the current URL.*/}
      <Route exact path='/' render={() => <Observer>{() => <Home store={store}/>}</Observer>}/>
      <Route exact path='/medusa_mcq' render={() => <Observer>{() => <MedusaMCQ store={store}/>}</Observer>}/>
    </Switch>
    }</Observer>

})
