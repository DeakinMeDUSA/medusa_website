import React from "react";
import styled from 'styled-components'
import { Composition } from 'atomic-layout'
import logo_lowres from '../media/logo_lowres.png'
import { Link } from "react-router-dom";
import { MdPersonPin } from "react-icons/md";
import { observer } from "mobx-react";
import { RootStore } from "../index";

const templateMobile = `
  logo menu user
  / 24px 1fr
`

const NavDiv = styled.div`
  background-color: #272f3e;
  border-radius: 3px;
  margin: 1em;
`
const StatusDiv = styled.div`
  color: red;
`
const NavLogo = styled.img`
  height: 4em;
  width: 4em;
  //alignment: left;
`
const NavItem = styled.li`
  padding-left: 20px;
  display: inline-block;
`;
const NavLink = styled(Link)`
  text-decoration: none;
  color: #d2d6dc;
`

const NavExtLink = styled.a`
  text-decoration: none;
  color: #d2d6dc;
`


const NavLinksList = styled.ul`
  list-style: none;
  display: flex;
  justify-content: flex-end;
  margin: 0;
  padding: 0;
`
const UserPin = styled(MdPersonPin)`
  color: white;
  height: 2em;
  width: 2em;
`

export const Menu = () => {
  return (
    <NavLinksList>
      <NavItem> <NavLink to={"/"}>Home</NavLink> </NavItem>
      {/*<NavItem> <NavLink to={"/"}>News</NavLink> </NavItem>*/}
      <NavItem> <NavLink to={"/about"}>About</NavLink> </NavItem>
      <NavItem> <NavExtLink href="https://www.facebook.com/pg/medusa.deakin/events">Events</NavExtLink> </NavItem>
      <NavItem> <NavLink to={"/members"}>Members</NavLink> </NavItem>
      <NavItem> <NavLink to={"/user"}>My Account</NavLink> </NavItem>
      <NavItem> <NavLink to={"/medusa_mcq"}>Medusa MCQ </NavLink> </NavItem>
    </NavLinksList>
  );
};


export const Navbar = observer(({ store }: { store: RootStore }) => {
  return (<>
      <Composition
        as={NavDiv}
        template={templateMobile}
        gap={20}
        padding={20}
        alignItems="center"
      >
        {(Areas) => (
          <>
            <Areas.Logo><NavLogo src={logo_lowres}/></Areas.Logo>
            <Areas.Menu justify="end">
              {/*<Only as={Menu} from="md" />*/}
              <Menu/>

            </Areas.Menu>
            <Areas.User justify="end"><UserPin/></Areas.User>


          </>
        )}

      </Composition>
      {/*<StatusDiv>Answers = {JSON.stringify(store.mcqStore.questions)}</StatusDiv>*/}
      {/*<StatusDiv>QuestionID = {JSON.stringify(store.mcqStore.curQuestionId)}</StatusDiv>*/}
      {/*<StatusDiv>showQuestionEdit = {JSON.stringify(store.mcqStore.showQuestionEdit)}</StatusDiv>*/}
    </>
  );
})
