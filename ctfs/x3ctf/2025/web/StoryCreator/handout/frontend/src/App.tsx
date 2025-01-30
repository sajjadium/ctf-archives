import { gql, useQuery } from "@apollo/client";
import styled from "@emotion/styled";
import { List, ListItemButton, ListItemText } from "@mui/material";
import React from "react";
import { NavLink, Outlet } from "react-router-dom";

const GridContainer = styled.div`
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 4fr;
  grid-template-rows: 1fr;
  gap: 0px 0px;
`;

const LeftNav = styled.div`
  grid-column: 1;
  grid-row: 1;
  background-color: #f0f0f0;
  padding: 1rem;
`;

const MainBody = styled.div`
  grid-column: 2;
  grid-row: 1;
  padding: 1rem;
`;

const LogoText = styled.h1`
  text-decoration: none;
  color: black;
  font-size: 24px;
  text-transform: uppercase;
`;

function NavButton(props: React.PropsWithChildren<{ to: string }>) {
  return (
    <NavLink to={props.to}>
      {({ isActive }) => (
        <ListItemButton selected={isActive}>
          <ListItemText
            sx={{
              color: "text.primary",
              textDecoration: "none",
            }}
          >
            {props.children}
          </ListItemText>
        </ListItemButton>
      )}
    </NavLink>
  );
}

function App() {
  const { loading, error, data } = useQuery(gql`
    {
      foo
    }
  `);

  if (loading) {
    return <p>Loading...</p>;
  }
  if (error) {
    return <p>Error: {error.message}</p>;
  }

  return (
    <GridContainer>
      <LeftNav>
        <NavLink to="/">
          <LogoText>Story Builder version {data.foo}</LogoText>
        </NavLink>

        <List component="nav">
          <NavButton to="/">My Stories</NavButton>
          <NavButton to="/exports">My Exports</NavButton>
          <NavButton to="/new">Create Story</NavButton>
          <NavButton to="/upload">Upload Image</NavButton>
          <NavButton to="/export">Export Story</NavButton>
        </List>
      </LeftNav>
      <MainBody>
        <Outlet />
      </MainBody>
    </GridContainer>
  );
}

export default App;
