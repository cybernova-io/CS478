import * as React from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import { red } from "@mui/material/colors";
import ImageOutlinedIcon from "@mui/icons-material/ImageOutlined";
import CardActions from "@mui/material/CardActions";
import Divider from "@mui/material/Divider";
import Stack from "@mui/material/Stack";
import ImageList from "@mui/material/ImageList";
import ImageListItem from "@mui/material/ImageListItem";
import ImageListItemBar from "@mui/material/ImageListItemBar";
import CancelIcon from "@mui/icons-material/Cancel";
import { useState, useEffect } from "react";
import { createPost } from "../../src/features/posts/postSlice";
import { styled } from "@mui/material/styles";
import IconButton from "@mui/material/IconButton";
import { useSelector, useDispatch } from "react-redux";
import { toast } from "react-toastify";

export default function PostForm() {
  const dispatch = useDispatch();

  const Input = styled("input")({
    display: "none",
  });

  const [postFormData, setPostFormData] = useState({
    text: "",
    photo: "",
  });
  const { text, photo } = postFormData;

  const [photoPreview, setPhotoPreview] = useState();

  useEffect(() => {
    if (photo) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhotoPreview(reader.result);
      };
      reader.readAsDataURL(photo);
    } else {
      setPhotoPreview(null);
    }
  }, [photo]);

  const handleInputChange = (e) => {
    const { name, value } = e.currentTarget;
    setPostFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };
  const handlePhoto = (e) => {
    setPostFormData({ ...postFormData, photo: e.target.files[0] });
  };

  const handlePhotoPreview = () => {
    setPostFormData({ ...postFormData, photo: "" });
    setPhotoPreview(null);
  };

  const onFormSubmit = (e) => {
    e.preventDefault();
    if (!text) {
      toast.error("Please enter a text.");
    } else {
      const formData = new FormData();
      formData.append("text", text);
      formData.append("photo", photo);
      dispatch(createPost(formData));

      setPostFormData({
        text: "",
        photo: "",
      });
      setPhotoPreview(null);
    }
  };

  return (
    <Grid item xs={12} sm={6} md={12}>
      <Card
        sx={{
          display: "flex",
          flexDirection: "column",
          maxWidth: 700,
          margin: "auto",
        }}
        component="form"
        onSubmit={onFormSubmit}
        encType="multipart/form-data"
        noValidate
      >
        <CardHeader
          title={
            <Typography variant="h5" component="div">
              Create Post
            </Typography>
          }
        />
        <Divider variant="middle" />
        <CardHeader
          avatar={
            <Avatar sx={{ bgcolor: red[500], width: 56, height: 56 }}>R</Avatar>
          }
          title={
            <TextField
              id="text"
              name="text"
              label="Write something here..."
              multiline
              variant="standard"
              rows={5}
              onChange={handleInputChange}
              value={text}
              fullWidth
            />
          }
        />

        {photo && (
          <ImageList
            sx={{
              // Promote the list into its own layer in Chrome. This costs memory, but helps keeping high FPS.
              p: 3,
              width: "100%",
              height: "100%",
            }}
          >
            <ImageListItem cols={12}>
              <img
                src={photoPreview}
                loading="lazy"
                sx={{
                  p: 3,
                }}
              />
              <ImageListItemBar
                sx={{
                  background:
                    "linear-gradient(to bottom, rgba(0,0,0,0.7) 0%, " +
                    "rgba(0,0,0,0.3) 70%, rgba(0,0,0,0) 100%)",
                }}
                position="top"
                actionIcon={
                  <IconButton
                    sx={{ color: "white", p: 2 }}
                    aria-label={`cancel`}
                    onClick={handlePhotoPreview}
                  >
                    <CancelIcon />
                  </IconButton>
                }
                actionPosition="right"
              />
            </ImageListItem>
          </ImageList>
        )}
        <CardActions
          sx={{
            display: "flex",
            justifyContent: "flex-end",
            m: 1,
          }}
        >
          <Stack spacing={2} direction="row">
            <label htmlFor="photo-image">
              <Input
                accept="image/*"
                id="photo-image"
                type="file"
                name="photo"
                onChange={handlePhoto}
              />
              <Button
                variant="outlined"
                startIcon={<ImageOutlinedIcon />}
                component="span"
              >
                Photo
              </Button>
            </label>
            <Button variant="outlined" type="submit">
              Post
            </Button>
          </Stack>
        </CardActions>
      </Card>
    </Grid>
  );
}
