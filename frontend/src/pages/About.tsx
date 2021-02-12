import React, { Component } from "react";
import { observer } from "mobx-react";
import { RootStore } from "../index";
import styled from "styled-components";
import { action, makeObservable, observable } from "mobx";
import { Button } from "react-bootstrap";
import { AboutSponsorText } from "../content/about/Sponsors";
import { AboutMainText } from "../content/about/Main";


export class AboutStore {
  rootStore: RootStore;
  showMain: boolean;
  showComStructure: boolean;
  showComCurrent: boolean;
  showComMeetings: boolean;
  showSubComs: boolean;
  showSponsors: boolean;
  showContactUs: boolean;

  constructor(rootStore: RootStore) {
    makeObservable(this, {
      showMain: observable,
      showComStructure: observable,
      showComCurrent: observable,
      showComMeetings: observable,
      showSubComs: observable,
      showSponsors: observable,
      showContactUs: observable,

      handle_toggle_show: action,
    })
    this.rootStore = rootStore
    this.showMain = false
    this.showComStructure = false
    this.showComCurrent = false
    this.showComMeetings = false
    this.showSubComs = false
    this.showSponsors = false
    this.showContactUs = false
  }


  handle_toggle_show(text_area: string) {
    console.log(`Changing area ${text_area}`)
    // @ts-ignore
    this[text_area] = !this[text_area]
  }
}

interface AccordionProps {
  readonly expanded: boolean;
}

const AccordionTitle = styled.span<AccordionProps>`
  padding: 1em 1.5em 1em 0;
  color: ${(props) => props.expanded ? "black" : "blue"};
`

const AccordionIcon = styled.span<AccordionProps>`
  display: inline-block;
  position: absolute;
  top: 18px;
  right: 0;
  width: 22px;
  height: 22px;
  border: 1px solid;
  border-radius: 22px;

  &::before {
    display: block;
    position: absolute;
    content: '';
    top: 9px;
    left: 5px;
    width: 10px;
    height: 2px;
    background: currentColor;
  }

  &::after {
    display: block;
    position: absolute;
    content: '';
    top: 5px;
    left: 9px;
    width: ${(props) => props.expanded ? '2px' : "0px"};
    height: 10px;
    background: currentColor;
  }
`

const AccordionButton = styled(Button)`
  //text-decoration: none;
  //width: 100%;
  //color: #d2d6dc;
  //
  //:hover {
  //  color: red;
  //}
  position: relative;
  display: block;
  text-align: left;
  width: 100%;
  padding: 1em 0;
  color: black;
  font-size: 1.15rem;
  font-weight: 400;
  border: none;
  background: none;
  outline: none;

  &:hover, &:focus {
    cursor: pointer;
    color: blue;

    &::after {
      cursor: pointer;
      color: blue;
      border: 1px solid blue;
    }
  }
`

const AboutDiv = styled.div`
  color: black;
  text-align: left;
  margin-left: auto;
  margin-right: auto;
  white-space: pre-wrap;
  max-width: 800px;


  box-sizing: border-box;

  &::before, &::after {
    box-sizing: border-box;
  }
`
const AccordionItem = styled.div`
  border-bottom: 1px solid lightgray;

  button[aria-expanded='true'] {
    border-bottom: 1px solid blue;
  }
`


const AccordianContent = styled.div<AccordionProps>`
  opacity: ${(props) => props.expanded ? 1 : 0};
  max-height: ${(props) => props.expanded ? '100%' : 0};
  overflow: hidden;
  transition: opacity 200ms linear, max-height 200ms linear;
  will-change: opacity, max-height;

  p {
    font-size: 1rem;
    font-weight: 300;
    margin: 2em 0;
  }
`

const areas = `
  header
  body
  footer
`
const Accordion = observer(({ store, sectionname, expanded, title, text }:
                              { store: AboutStore, sectionname: string, expanded: boolean, title: string, text: any }) => {
  return (
    <AccordionItem>
      <AccordionButton onClick={() => store.handle_toggle_show(sectionname)}>
        <AccordionTitle expanded={expanded}>{title}</AccordionTitle>
        <AccordionIcon expanded={expanded}/>
      </AccordionButton>
      <AccordianContent expanded={expanded}>{text}</AccordianContent>
    </AccordionItem>
  )
})



export const About = observer(({ store }: { store: RootStore }) => {
  return (
    <AboutDiv>
      <Accordion store={store.aboutStore} expanded={store.aboutStore.showMain} title={"Main Title"}
                 sectionname={"showMain"} text={<AboutMainText/>}/>

      <Accordion store={store.aboutStore} expanded={store.aboutStore.showMain} title={"Main Title"}
                 sectionname={"showMain"} text={<AboutMainText/>}/>
      <Accordion store={store.aboutStore} expanded={store.aboutStore.showMain} title={"Main Title"}
                 sectionname={"showMain"} text={<AboutMainText/>}/>
      <Accordion store={store.aboutStore} expanded={store.aboutStore.showMain} title={"Main Title"}
                 sectionname={"showMain"} text={<AboutMainText/>}/>

      <div>"Some more body text"</div>
      <AboutSponsorText/>

    </AboutDiv>
  )
})
