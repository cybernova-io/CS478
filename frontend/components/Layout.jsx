import * as React from "react";
import CssBaseline from "@mui/material/CssBaseline";
import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import Header from "./Header";
import { createTheme, ThemeProvider } from "@mui/material/styles";

export default function Layout(props) {
  return (
    <>
      <Header />
      <main>
        <Container sx={{ py: 5 }} maxWidth="md">
          <Grid container spacing={4}>
            {props.children}
          </Grid>
        </Container>
      </main>
    </>
  );
}
