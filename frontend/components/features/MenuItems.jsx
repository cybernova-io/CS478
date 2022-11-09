import * as React from "react";
import { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import ListItemText from "@mui/material/ListItemText";
import ListItemIcon from "@mui/material/ListItemIcon";
import IconButton from "@mui/material/IconButton";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import EditPostForm from "../post/EditPostForm";
import DeleteDialog from "../alert-box/DeleteDialog";
import BookmarkIcon from "@mui/icons-material/Bookmark";
import { savePost } from "./posts/postSlice";
import { toast } from "react-toastify";

export default function MenuItems(props) {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);

  const [editPostForm, setEditPostForm] = useState(false);

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

  const toggleEditPostModal = () => {
    setEditPostForm((prevData) => !prevData);
  };

  // Identify component type
  let onClickEditMenu;

  if (props.componentType === "post") {
    onClickEditMenu = toggleEditPostModal;
  } else if (props.componentType === "comment") {
    onClickEditMenu = () => props.componentFunc(props.componentData._id);
  }

  const handleSaveClick = (postId) => {
    var saveData = {
      userId: user._id,
      postId: postId,
    };

    dispatch(savePost(saveData));
    setAnchorEl(null);
    props.componentData.saves.userId.some((id) => id === user._id)
      ? toast.info("Post unsaved.")
      : toast.success("Post saved.");
  };

  return (
    <>
      <IconButton
        aria-label="more"
        id="long-button"
        aria-controls={openOptions ? "long-menu" : undefined}
        aria-expanded={openOptions ? "true" : undefined}
        aria-haspopup="true"
        onClick={handleClickOptions}
        sx={{ color: "gray" }}
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
        {props.componentData.user === user._id && (
          <MenuItem onClick={onClickEditMenu}>
            <ListItemIcon>
              <EditIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Edit</ListItemText>
          </MenuItem>
        )}
        {props.componentData.user === user._id && (
          <EditPostForm
            key={props.componentData._id}
            editPostForm={editPostForm}
            toggleEditPostModal={toggleEditPostModal}
            handleCloseOptions={handleCloseOptions}
            postData={props.componentData}
          />
        )}

        {props.componentType === "post" && (
          <MenuItem onClick={() => handleSaveClick(props.componentData._id)}>
            <ListItemIcon>
              <BookmarkIcon fontSize="small" />
            </ListItemIcon>
            {props.componentData.saves.userId.some((id) => id === user._id) ? (
              <ListItemText>Unsave Post</ListItemText>
            ) : (
              <ListItemText>Save Post</ListItemText>
            )}
          </MenuItem>
        )}

        {props.componentData.user === user._id && (
          <MenuItem onClick={handleDeleteDialog}>
            <ListItemIcon>
              <DeleteIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Delete</ListItemText>
          </MenuItem>
        )}

        {props.componentData.user === user._id && (
          <DeleteDialog
            deleteDialog={deleteDialog}
            componentData={props.componentData}
            componentType={props.componentType}
            handleDeleteDialog={handleDeleteDialog}
          />
        )}
      </Menu>
    </>
  );
}
