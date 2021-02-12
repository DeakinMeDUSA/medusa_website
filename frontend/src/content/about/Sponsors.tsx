import styled from "styled-components";
import dusa from "../../media/about/sponsors/dusa.png";
import { Composition } from "atomic-layout";

const MainTextStyle = styled.div`
  //float: right;
`
const SponsorLogo = styled.img`
  max-height: 200px;
  max-width: 150px;

`
const areasSponsors = `
  logo
`

export const AboutSponsorText = () => {
  return (
    <MainTextStyle>
      <div>MeDUSA acknowledges the kind and generous support from all our sponsors <br/><br/></div>


      <Composition areas={areasSponsors}>
        {({ Logo }) => (
          <>
            <Logo><SponsorLogo src={dusa}/></Logo>

          </>
        )}
      </Composition>

    </MainTextStyle>
  )
}
