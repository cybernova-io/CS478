import * as React from "react";
import { useState, useEffect } from "react";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import { useDispatch } from "react-redux";
import { updatePost } from "../../src/features/posts/postSlice";
import DialogTitle from "@mui/material/DialogTitle";
import { styled } from "@mui/material/styles";
import Stack from "@mui/material/Stack";
import ImageOutlinedIcon from "@mui/icons-material/ImageOutlined";
import ImageList from "@mui/material/ImageList";
import ImageListItem from "@mui/material/ImageListItem";
import ImageListItemBar from "@mui/material/ImageListItemBar";
import IconButton from "@mui/material/IconButton";
import CancelIcon from "@mui/icons-material/Cancel";
import PropTypes from "prop-types";
import CloseIcon from "@mui/icons-material/Close";
import { toast } from "react-toastify";

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  "& .MuiDialogContent-root": {
    padding: theme.spacing(2),
    width: 600,
  },
  "& .MuiDialogActions-root": {
    padding: theme.spacing(1),
  },
}));

const BootstrapDialogTitle = (props) => {
  const { children, onClose, ...other } = props;

  return (
    <DialogTitle sx={{ m: 0, p: 2 }} {...other}>
      {children}
      {onClose ? (
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{
            position: "absolute",
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
      ) : null}
    </DialogTitle>
  );
};

BootstrapDialogTitle.propTypes = {
  children: PropTypes.node,
  onClose: PropTypes.func.isRequired,
};

export default function EditPost(props) {
  const dispatch = useDispatch();

  const Input = styled("input")({
    display: "none",
  });

  const [editPostData, setEditPostData] = useState({
    postId: props.postData._id,
    editText: props.postData.text,
    editPhoto: props.postData.photo,
  });

  const { postId, editText, editPhoto } = editPostData;

  const [editPhotoPreview, setEditPhotoPreview] = useState(editPhoto);

  useEffect(() => {
    if (editPhoto instanceof Blob) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setEditPhotoPreview(reader.result);
      };
      reader.readAsDataURL(editPhoto);
    }
  }, [editPhoto]);

  const handleEditInputChange = (e) => {
    const { name, value } = e.currentTarget;
    setEditPostData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleEditPhoto = (e) => {
    setEditPostData({ ...editPostData, editPhoto: e.target.files[0] });
  };

  const handleEditChangePreview = () => {
    setEditPostData({ ...editPostData, editPhoto: "" });
    setEditPhotoPreview(null);
  };

  const onEditFormSubmit = (e) => {
    e.preventDefault();

    if (!editText) {
      toast.error("Please enter a text.");
    } else {
      const formData = new FormData();
      formData.append("text", editText);
      editPhoto !== null && formData.append("photo", editPhoto);

      dispatch(updatePost({ postId, formData }));
    }
  };

  return (
    <BootstrapDialog
      onClose={props.toggleEditPostModal}
      aria-labelledby="customized-dialog-title"
      open={props.editPostForm}
      component="form"
      onSubmit={onEditFormSubmit}
      encType="multipart/form-data"
      noValidate
    >
      <BootstrapDialogTitle
        id="customized-dialog-title"
        onClose={props.toggleEditPostModal}
      >
        Edit Post
      </BootstrapDialogTitle>
      <DialogContent dividers>
        <TextField
          autoFocus
          name="editText"
          label="Write something here..."
          variant="standard"
          rows={5}
          onChange={handleEditInputChange}
          value={editText}
          fullWidth
          multiline
        />
        {editPhoto && (
          <ImageList
            sx={{
              width: "100%",
              height: "100%",
            }}
          >
            <ImageListItem cols={12}>
              <img
                src={
                  editPhoto instanceof Blob
                    ? editPhotoPreview
                    : `uploads/${editPhotoPreview}`
                }
                loading="lazy"
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
                    onClick={handleEditChangePreview}
                  >
                    <CancelIcon />
                  </IconButton>
                }
                actionPosition="right"
              />
            </ImageListItem>
          </ImageList>
        )}
      </DialogContent>
      <DialogActions
        sx={{
          m: 1,
        }}
        disableSpacing
      >
        <Stack spacing={2} direction="row">
          <label htmlFor="update-photo-image">
            <Input
              accept="image/*"
              id="update-photo-image"
              type="file"
              name="editPhoto"
              onChange={handleEditPhoto}
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
      </DialogActions>
    </BootstrapDialog>
  );
}
