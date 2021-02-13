import { Route, Switch } from 'react-router-dom';

import { Observer, observer } from "mobx-react";
import { Home } from '../pages/Home';
import { RootStore } from "./RootStore";
import { MedusaMCQ } from "../pages/MedusaMCQ";
import { About } from "../pages/About";
import { Members } from "../pages/Members";
import { UserPage } from "../pages/User";
import React from 'react';

export const Main = observer(({ store }: { store: RootStore }) => {
  return <Observer>{() =>
    <Switch> {/* The Switch decides which component to show based on the current URL.*/}
      <Route exact path='' render={() => <Observer>{() => <Home store={store}/>}</Observer>}/>
      <Route exact path='/about' render={() => <Observer>{() => <About store={store}/>}</Observer>}/>
      <Route exact path='/members' render={() => <Observer>{() => <Members store={store}/>}</Observer>}/>
      <Route exact path='/user' render={() => <Observer>{() => <UserPage store={store}/>}</Observer>}/>
      <Route exact path='/medusa_mcq' render={() => <Observer>{() => <MedusaMCQ store={store}/>}</Observer>}/>
    </Switch>
  }</Observer>

})
