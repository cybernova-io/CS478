import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useRouter } from "next/router";
import Layout from "../components/Layout";
import Box from "@mui/material/Box";
import Avatar from "@mui/material/Avatar";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import { updateUser } from "../src/features/auth/authSlice";
import { styled } from "@mui/material/styles";
import { toast } from "react-toastify";
import ImageOutlinedIcon from "@mui/icons-material/ImageOutlined";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Stack from "@mui/material/Stack";

Account.title = "Screagles Connect: Account";

export default function Account() {
  const dispatch = useDispatch();
  const router = useRouter();

  const Input = styled("input")({
    display: "none",
  });

  const { user, isLoading, isError, isSuccess, message } = useSelector(
    (state) => state.auth
  );

  const [userFormData, setUserFormData] = useState({
    firstName: user ? user.firstName : "",
    lastName: user ? user.lastName : "",
    photo: user ? user.photo : "",
    email: user ? user.email : "",
    password: "",
    confirmPassword: "",
  });

  const { firstName, lastName, email, photo, password, confirmPassword } =
    userFormData;

  const [photoPreview, setPhotoPreview] = useState(`/uploads/${photo}`);

  useEffect(() => {
    if (isError) {
      toast.error(message);
    }

    if (photo instanceof Blob) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhotoPreview(reader.result);
      };
      reader.readAsDataURL(photo);
    }

    localStorage.setItem("user", JSON.stringify(user));
  }, [user, photo, router, dispatch]);

  const handleInputChange = (e) => {
    const { name, value } = e.currentTarget;
    setUserFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handlePhoto = (e) => {
    setUserFormData({ ...userFormData, photo: e.target.files[0] });
  };

  const handleEditChangePreview = () => {
    setUserFormData({ ...userFormData, photo: "" });
    setPhotoPreview(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("lastName", lastName);
    formData.append("firstName", firstName);
    photo !== null && formData.append("photo", photo);
    if (password || confirmPassword) {
      if (password !== confirmPassword) {
        toast.error("Passwords do not match!");
      } else {
        formData.append("password", password);
        dispatch(updateUser(formData));
        setUserFormData({
          ...userFormData,
          password: "",
          confirmPassword: "",
        });
        toast.success("Account updated.");
      }
    } else {
      dispatch(updateUser(formData));
      toast.success("Account updated.");
    }
  };

  return (
    <Layout>
      <Box
        component="form"
        onSubmit={handleSubmit}
        encType="multipart/form-data"
        noValidate
        sx={{ width: "100%", margin: "auto", pl: 2 }}
      >
        <Card>
          <CardContent>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={12} sx={{ mb: 2 }}>
                <Stack
                  spacing={2}
                  direction="row"
                  justifyContent="flex-start"
                  alignItems="flex-end"
                >
                  {photo ? (
                    <Avatar
                      sx={{
                        width: 150,
                        height: 150,
                      }}
                      src={photoPreview}
                    />
                  ) : (
                    <Avatar sx={{ width: 150, height: 150 }} />
                  )}
                  <label htmlFor="update-photo-image">
                    <Input
                      accept="image/*"
                      id="update-photo-image"
                      type="file"
                      name="photo"
                      onChange={handlePhoto}
                    />
                    <Button
                      variant="contained"
                      size="small"
                      startIcon={<ImageOutlinedIcon />}
                      component="span"
                    >
                      Change
                    </Button>
                  </label>
                </Stack>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  autoComplete="given-name"
                  name="firstName"
                  required
                  fullWidth
                  id="firstName"
                  label="First Name"
                  onChange={handleInputChange}
                  value={firstName}
                  autoFocus
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  id="lastName"
                  label="Last Name"
                  name="lastName"
                  autoComplete="family-name"
                  onChange={handleInputChange}
                  value={lastName}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  id="email"
                  label="Email Address"
                  name="email"
                  autoComplete="email"
                  value={email}
                  disabled
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  name="password"
                  label="New Password"
                  type="password"
                  id="password"
                  autoComplete="new-password"
                  onChange={handleInputChange}
                  value={password}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  name="confirmPassword"
                  label="Confirm New Password"
                  type="password"
                  id="confirmPassword"
                  onChange={handleInputChange}
                  value={confirmPassword}
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Update
            </Button>
          </CardContent>
        </Card>
      </Box>
    </Layout>
  );
}
