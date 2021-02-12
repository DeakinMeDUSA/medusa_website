import styled from "styled-components";
import { observer } from "mobx-react";
import { RootStore } from "../index";
import React from "react";

export const User = observer(({ store }: { store: RootStore }) => {
  return (
    <div>This is the User page
    </div>
  );
})
