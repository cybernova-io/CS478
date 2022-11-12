import * as React from "react";
import { useState, useEffect } from "react";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Link from "@mui/material/Link";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { login, reset } from "../src/features/auth/authSlice";
import Spinner from "../components/Spinner";
import { useSelector, useDispatch } from "react-redux";
import { useRouter } from "next/router";
import { toast } from "react-toastify";
import ImageList from "@mui/material/ImageList";
import ImageListItem from "@mui/material/ImageListItem";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";

const theme = createTheme();

SignIn.title = "Screagles Connect: Sign in";

export default function SignIn() {
  const [userFormData, setUserFormData] = useState({
    email: "",
    password: "",
  });

  const { email, password } = userFormData;

  const [account, setAccount] = useState("");

  const handleSelectChange = (event) => {
    setUserFormData({
      email: `${event.target.value}@gmail.com`,
      password: `${event.target.value}`,
    });
    setAccount(event.target.value);
  };

  const router = useRouter();
  const dispatch = useDispatch();

  const { user, isLoading, isError, isSuccess, message } = useSelector(
    (state) => state.auth
  );

  useEffect(() => {
    if (isError) {
      toast.error(message);
    }

    if (isSuccess || user) {
      router.push("/home");
    }

    dispatch(reset());
  }, [user, isError, isSuccess, message, router, dispatch]);

  const handleInputChange = (e) => {
    const { name, value } = e.currentTarget;
    setUserFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const userData = {
      email,
      password,
    };

    dispatch(login(userData));
  };

  if (isLoading) {
    return <Spinner />;
  }

  return (
    <ThemeProvider theme={theme}>
      <Grid container component="main" sx={{ height: "100vh" }}>
        <CssBaseline />
        <Grid
          item
          xs={false}
          sm={4}
          md={6}
          sx={{
            backgroundImage: "url(/images/bckgr1.png)",
            backgroundRepeat: "no-repeat",
            backgroundColor: (t) =>
              t.palette.mode === "light"
                ? t.palette.grey[50]
                : t.palette.grey[900],
            backgroundSize: "contain",
            backgroundPosition: "center",
          }}
        />
        <Grid item xs={12} sm={7} md={4} component={Paper} elevation={6} square>
          <Box
            sx={{
              my: 8,
              mx: 4,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <ImageList
              sx={{
                width: "70%",
                height: "70%",
              }}
            >
              <ImageListItem cols={12}>
                <img src={`/logos/eagle5.png`} loading="lazy" />
              </ImageListItem>
            </ImageList>
            <Typography component="h1" variant="h5">
              Sign in
            </Typography>
            <Box
              component="form"
              noValidate
              onSubmit={handleSubmit}
              sx={{ mt: 1 }}
            >
              <TextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                onChange={handleInputChange}
                value={email}
                autoFocus
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
                onChange={handleInputChange}
                value={password}
              />
              <FormControl fullWidth sx={{ mt: 2 }}>
                <InputLabel id="simple-select-label">Sample Users</InputLabel>
                <Select
                  labelId="simple-select-label"
                  id="simple-select"
                  value={account}
                  label="Sample Users"
                  onChange={handleSelectChange}
                >
                  {[1, 2, 3, 4, 5].map((num) => {
                    return (
                      <MenuItem key={num} value={num}>
                        User {`${num}`}
                      </MenuItem>
                    );
                  })}
                </Select>
              </FormControl>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Sign In
              </Button>
              <Grid container>
                <Grid item>
                  <Link href="/register" variant="body2">
                    {"Don't have an account? Sign Up"}
                  </Link>
                </Grid>
              </Grid>
            </Box>
          </Box>
        </Grid>
        <Grid
          item
          xs={false}
          sm={1}
          md={2}
          sx={{
            backgroundColor: "primary.main",
          }}
        />
      </Grid>
    </ThemeProvider>
  );
}
