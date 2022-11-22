import * as React from "react";
import CssBaseline from "@mui/material/CssBaseline";
import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import Header from "./Header";
import { useSelector, useDispatch } from "react-redux";

export default function Layout(props) {
  const { user } = useSelector((state) => state.auth);
  var isUser = JSON.parse(localStorage.getItem("user"));

  if (!isUser) {
    router.push("/");
  }

  return (
    <>
      {user && <Header />}
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
