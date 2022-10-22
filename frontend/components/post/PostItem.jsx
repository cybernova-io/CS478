import * as React from "react";
import { useState, useEffect } from "react";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Collapse from "@mui/material/Collapse";
import Avatar from "@mui/material/Avatar";
import IconButton from "@mui/material/IconButton";
import { red } from "@mui/material/colors";
import FavoriteIcon from "@mui/icons-material/Favorite";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import Grid from "@mui/material/Grid";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import ListItemText from "@mui/material/ListItemText";
import ListItemIcon from "@mui/material/ListItemIcon";
import EditPostForm from "./EditPostForm";
import { useSelector, useDispatch } from "react-redux";
import DeleteDialog from "../alert-box/DeleteDialog";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";
import TimeAgo from "javascript-time-ago";
import en from "javascript-time-ago/locale/en.json";
import CommentForm from "./CommentForm";
import CommentItem from "./CommentItem";
import ReadMore from "../../src/features/Readmore";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import { getComments, reset } from "../../src/features/comments/commentSlice";

TimeAgo.addDefaultLocale(en);

export default function PostItem({ post }) {
  const dispatch = useDispatch();
  const timeAgo = new TimeAgo("en-US");

  const { comments } = useSelector((state) => state.comments);
  const commentsInitialState = comments.map((obj) => ({
    ...obj,
    isEditing: false,
  }));
  const [commentsItem, setCommentsItem] = useState(commentsInitialState);
  const [editPostForm, setEditPostForm] = useState(false);

  let commentNum = 0;
  comments.map((comment) => post._id === comment.postId && commentNum++);

  useEffect(() => {
    dispatch(getComments());

    setCommentsItem(commentsInitialState);

    // return () => {
    // 	dispatch(reset());
    // };
  }, [dispatch, JSON.stringify(comments)]);

  const [deleteDialog, setdeleteDialog] = React.useState(false);

  const [expanded, setExpanded] = React.useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const [anchorEl, setAnchorEl] = React.useState(null);

  const openOptions = Boolean(anchorEl);

  const handleClickOptions = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleCloseOptions = () => {
    setAnchorEl(null);
  };

  const toggleEditPostModal = () => {
    setEditPostForm((prevData) => !prevData);
  };

  const handleDeleteDialog = () => {
    setdeleteDialog((prevData) => !prevData);
  };

  const handleEditComment = (commentId) => {
    setCommentsItem(
      commentsItem.map((data) => {
        return data._id === commentId
          ? { ...data, isEditing: !data.isEditing }
          : { ...data, isEditing: false };
      })
    );
  };

  return (
    <Grid item xs={12} sm={6} md={12}>
      <Card
        sx={{
          display: "flex",
          flexDirection: "column",
          maxWidth: 700,
          margin: "auto",
          wordWrap: "break-word",
        }}
      >
        <CardHeader
          avatar={
            <Avatar sx={{ bgcolor: red[500] }} aria-label="avatar">
              R
            </Avatar>
          }
          action={
            <>
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
                <MenuItem onClick={toggleEditPostModal}>
                  <ListItemIcon>
                    <EditIcon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText>Edit</ListItemText>
                </MenuItem>
                <EditPostForm
                  key={post._id}
                  editPostForm={editPostForm}
                  toggleEditPostModal={toggleEditPostModal}
                  componentData={post}
                  componentType="post"
                />
                <MenuItem onClick={handleDeleteDialog}>
                  <ListItemIcon>
                    <DeleteIcon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText>Delete</ListItemText>
                </MenuItem>
                <DeleteDialog
                  deleteDialog={deleteDialog}
                  postData={post}
                  handleDeleteDialog={handleDeleteDialog}
                />
              </Menu>
            </>
          }
          title="Shrimp and Chorizo Paella"
          subheader={timeAgo.format(new Date(post.createdAt))}
        />
        <CardContent>
          <ReadMore>{post.text}</ReadMore>
        </CardContent>
        {post.photo && (
          <CardMedia
            component="img"
            image={`/uploads/${post.photo}`}
            alt={post.photo}
          />
        )}
        <CardActions disableSpacing>
          <IconButton aria-label="add to favorites">
            <FavoriteIcon />
          </IconButton>
          <IconButton aria-label="like">
            <ThumbUpIcon />
          </IconButton>
          <Button
            sx={{ marginLeft: "auto", textTransform: "capitalize" }}
            onClick={handleExpandClick}
            variant="text"
          >
            {commentNum} Comments
          </Button>
        </CardActions>
        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <Divider variant="middle" />
          {commentsItem.map(
            (commentItem) =>
              post._id === commentItem.postId && (
                <CommentItem
                  key={commentItem._id}
                  commentData={commentItem}
                  postData={post}
                  handleEditComment={handleEditComment}
                />
              )
          )}

          <Divider variant="middle" />
          <CommentForm postData={post} />
        </Collapse>
      </Card>
    </Grid>
  );
}
