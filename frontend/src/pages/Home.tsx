import React from "react";
import { observer } from "mobx-react";
import { RootStore } from "../index";

export const Home = observer(({ store }: { store: RootStore }) => {
  return (
    <div>This is the Home page
      <div>API Root URL : {store.mcqStore.api.rootURL}</div>
      <div>Answers : {JSON.stringify(store.mcqStore.answers)}</div>
    </div>
    //  TODO use https://instafeedjs.com/#/?id=instafeedjs
  );
})

