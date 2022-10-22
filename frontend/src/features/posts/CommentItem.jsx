import * as React from "react";
import { useState } from "react";
import Avatar from "@mui/material/Avatar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import { red } from "@mui/material/colors";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import Grid from "@mui/material/Grid";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import ListItemText from "@mui/material/ListItemText";
import ListItemIcon from "@mui/material/ListItemIcon";
import { useDispatch } from "react-redux";
import DeleteDialog from "../alert-box/DeleteDialog";
import TextField from "@mui/material/TextField";
import { updateComment } from "../../src/features/comments/commentSlice";
import ReadMore from "../features/Readmore";
import Box from "@mui/material/Box";
import TimeAgo from "javascript-time-ago";
import en from "javascript-time-ago/locale/en.json";
import Paper from "@mui/material/Paper";
import { toast } from "react-toastify";

TimeAgo.addDefaultLocale(en);

export default function PostItem(props) {
  const dispatch = useDispatch();
  const timeAgo = new TimeAgo("en-US");

  const [deleteDialog, setdeleteDialog] = React.useState(false);

  const [anchorEl, setAnchorEl] = React.useState(null);

  const openOptions = Boolean(anchorEl);

  const handleClickOptions = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleCloseOptions = () => {
    setAnchorEl(null);
  };

  const handleDeleteDialog = () => {
    setdeleteDialog((prevData) => !prevData);
  };

  const [commentFormData, setCommentFormData] = useState({
    postId: props.postData._id,
    commentId: props.commentData._id,
    comment: props.commentData.comment,
  });

  const { commentId, comment } = commentFormData;

  const handleInputChange = (e) => {
    const { name, value } = e.currentTarget;
    setCommentFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const onFormSubmit = (e) => {
    e.preventDefault();
    if (!comment) {
      toast.error("Please enter a text.");
    } else {
      dispatch(updateComment({ commentId, commentFormData }));
      handleEditMenu(commentId);
    }
  };

  const handleEditMenu = (commentId) => {
    setAnchorEl(null);
    return props.handleEditComment(commentId);
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Grid container wrap="nowrap" spacing={2}>
        <Grid item>
          <Avatar
            sx={{ bgcolor: red[500], width: 30, height: 30 }}
            aria-label="avatar"
          >
            R
          </Avatar>
        </Grid>
        {props.commentData.isEditing ? (
          <Grid item xs zeroMinWidth>
            <Box
              component="form"
              onSubmit={onFormSubmit}
              noValidate
              autoComplete="off"
            >
              <TextField
                name="comment"
                label="Write something here..."
                variant="filled"
                onChange={handleInputChange}
                value={comment}
                size="small"
                fullWidth
              />
            </Box>
            <Typography
              variant="caption"
              sx={{ p: 1.3 }}
              color="text.secondary"
            >
              Press Enter to save.
            </Typography>
          </Grid>
        ) : (
          <>
            <Grid justifyContent="left" item xs zeroMinWidth>
              <Box
                sx={{
                  backgroundColor: (theme) =>
                    theme.palette.mode === "light"
                      ? theme.palette.grey[200]
                      : theme.palette.grey[800],
                  p: 1.3,
                  borderRadius: 5,
                  width: "max-content",
                  maxWidth: 590,
                  whiteSpace: "pre-wrap",
                  wordWrap: "break-word",
                }}
              >
                <Typography variant="body2" sx={{ fontWeight: "bold" }}>
                  Michael Weldon
                </Typography>
                <ReadMore>{props.commentData.comment}</ReadMore>
              </Box>
              <Typography
                variant="caption"
                sx={{ p: 1.3 }}
                color="text.secondary"
              >
                {timeAgo.format(new Date(props.commentData.createdAt))}
              </Typography>
            </Grid>
            <Grid item>
              <Box sx={{ float: "left" }}>
                <IconButton
                  aria-label="more"
                  id="long-button"
                  aria-controls={openOptions ? "long-menu" : undefined}
                  aria-expanded={openOptions ? "true" : undefined}
                  aria-haspopup="true"
                  onClick={handleClickOptions}
                >
                  <MoreVertIcon />
                </IconButton>
                <Menu
                  id="long-menu"
                  MenuListProps={{
                    "aria-labelledby": "menu-button",
                  }}
                  anchorEl={anchorEl}
                  open={openOptions}
                  onClose={handleCloseOptions}
                  PaperProps={{
                    style: {
                      width: "20ch",
                    },
                  }}
                >
                  <MenuItem
                    onClick={() => handleEditMenu(props.commentData._id)}
                  >
                    <ListItemIcon>
                      <EditIcon fontSize="small" />
                    </ListItemIcon>
                    <ListItemText>Edit</ListItemText>
                  </MenuItem>
                  <MenuItem onClick={handleDeleteDialog}>
                    <ListItemIcon>
                      <DeleteIcon fontSize="small" />
                    </ListItemIcon>
                    <ListItemText>Delete</ListItemText>
                  </MenuItem>
                  <DeleteDialog
                    deleteDialog={deleteDialog}
                    componentData={props.commentData}
                    componentType="comment"
                    handleDeleteDialog={handleDeleteDialog}
                  />
                </Menu>
              </Box>
            </Grid>
          </>
        )}
      </Grid>
    </Paper>
  );
}
