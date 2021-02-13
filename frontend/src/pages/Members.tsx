import React from "react";
import { observer } from "mobx-react";
import { RootStore } from "../components/RootStore";

export const Members = observer(({ store }: { store: RootStore }) => {
  return (
    <div>This is the Members page
    </div>
  );
})
