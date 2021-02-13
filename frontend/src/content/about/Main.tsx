import React from "react";
import styled from "styled-components";
import school_of_med from "../../media/about/main/school_of_med.jpg"

const MainTextStyle = styled.div`
  //float: right;
`
const SchoolOfMedDiv = styled.img`
  float: right;

`

export const AboutMainText = () => {
  return (
    <MainTextStyle>
      <SchoolOfMedDiv src={school_of_med}/>
      <b>MeDUSA is your medical society that represents you!</b><br/><br/>

      MeDUSA aims to support all Deakin medical students and enhance your medical student experience. We have numerous
      domains, at least one of which will interest everybody. From academic advocacy and policies to community
      involvement and enormous social events, we aim to provide the best possible experience we can for our student
      body. <br/><br/>

      The first cohort of students to enter Deakin Medical School established MeDUSA in 2008. Acknowledgements must be
      made to Caroline Bate, who was MeDUSA’s founding President. Caroline, along with a dedicated team of like minded
      medical students, laid the crucial groundwork of the committee for years to come.<br/><br/>

      MeDUSA’s advocates for students in various aspects of their medical curriculum. This includes student
      representation within committees of the School of Medicine (SoM), such as the Teaching and Learning Committee
      (TLC) and Student
      Advisory Board for the Faculty of Health. Additionally, MeDUSA networks with other organisations and stakeholders
      relevant to your medical career such as the Australian Medical Students’ Association (AMSA), the Australian
      Medical
      Association (AMA) and the Postgraduate Medical Council of Victoria.<br/><br/>

      MeDUSA has regular meetings with curriculum theme leaders, as well as the Head of School. The committee is
      structured to include members from all year levels. This ensures that all cohorts are equally represented and
      student concerns are addressed appropriately. MeDUSA also endeavours to provide students with valuable online
      resources, which can be utilised by students at all clinical sites.<br/><br/>

      One of MeDUSA’s main objectives is to enrich the Deakin medical experience and foster relationships that will last
      a
      lifetime. Our annual social events, including Cocktail Night, MedCamp, MedBall and GradBall, will make your time
      at
      medical school unforgettable! In addition, the preclinical and clinical committees provide academic, social and
      community initiatives that are tailored to the specific groups they represent.<br/><br/>

      MeDUSA has a growing number of special interest subcommittees, which encourage like-minded people to explore
      particular areas of medicine and health together. In addition, we have close relationships with other health
      organisations such as Universal Health at Deakin (UHAD), General Practice Student Network (GPSN) and Nursing,
      Occupational Therapy, Medicine and Allied Health at Deakin (NOMAD).<br/><br/>

      MeDUSA is an incorporated organisation that is registered with the Department of Consumer and Employment
      Protection.
      As such, MeDUSA abides by a constitution and a set of register of resolutions. These documents include details
      about
      the MeDUSA committee structure, election processes, annual general meeting requirements and the responsibilities
      of
      members. These documents can be requested from the MeDUSA Secretary, so that you, as a member of the student body,
      can further your understanding of the functioning of MeDUSA as an organisation.<br/><br/>

      The current MeDUSA committee would like to encourage you, the Deakin medical student, to explore your interests
      and
      become involved in the areas of medical school that inspire, concern or motivate you. Not only can you develop
      your
      leadership skills and meet your senior peers, but you can engage with issues pertinent to your future medical
      career. Best of all, it means that YOU can make a difference.<br/><br/>

      <b>FUN FACT: What’s in the name?</b><br/>
      MeDUSA is a portmanteau of “Medical” and “DUSA” (Deakin University Students’ Association)” (Medical + DUSA =
      MeDUSA). Other than having a snake in our logo, MeDUSA has no other relationship to the Greek myth, a “monster….
      generally described as having a face of a hideous human female with living venomous snakes in place of hair”.
      MeDUSA
      believes that none of our Deakin medical students resemble her, however some may beg to differ during exam period!

    </MainTextStyle>
  )
}
