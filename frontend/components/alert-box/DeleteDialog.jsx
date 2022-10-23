import * as React from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import { useDispatch } from "react-redux";
import { deletePost } from "../../src/features/posts/postSlice";
import { deleteComment } from "../../src/features/comments/commentSlice";

export default function DeleteDialog(props) {
  const dispatch = useDispatch();

  const handleDeleteButton = () => {
    if (props.componentType === "post") {
      var postId = props.componentData._id;
      var postPhoto = props.componentData.photo;
      dispatch(deletePost({ postId, postPhoto }));
    } else if (props.componentType === "comment") {
      var commentId = props.componentData._id;
      dispatch(deleteComment(commentId));
    }
  };

  return (
    <Dialog
      open={props.deleteDialog}
      onClose={props.handleDeleteDialog}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle id="alert-dialog-title">{"Delete this post?"}</DialogTitle>
      <DialogContent>
        <DialogContentText id="alert-dialog-description">
          Are you sure you want to delete this post?
        </DialogContentText>
      </DialogContent>
      <DialogActions
        sx={{
          m: 1,
        }}
      >
        <Button onClick={props.handleDeleteDialog}>Cancel</Button>
        <Button onClick={handleDeleteButton} variant="contained" autoFocus>
          Proceed
        </Button>
      </DialogActions>
    </Dialog>
  );
}
