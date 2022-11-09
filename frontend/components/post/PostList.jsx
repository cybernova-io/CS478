import * as React from "react";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Collapse from "@mui/material/Collapse";
import Avatar from "@mui/material/Avatar";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";
import CommentForm from "../comment/CommentForm";
import CommentList from "../comment/CommentList";
import MenuItems from "../../components/features/MenuItems";
import ReadMore from "../../components/features/ReadMore";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import RecommendIcon from "@mui/icons-material/Recommend";
import ThumbUpOutlinedIcon from "@mui/icons-material/ThumbUpOutlined";
import ChatBubbleOutlineOutlinedIcon from "@mui/icons-material/ChatBubbleOutlineOutlined";
import { getComments } from "../../src/features/comments/commentSlice";
import LikesModal from "../like/LikesModal";
import Box from "@mui/material/Box";
import PublicIcon from "@mui/icons-material/Public";
import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import Stack from "@mui/material/Stack";
import Tooltip from "@mui/material/Tooltip";
import { likePost } from "../../src/features/posts/postSlice";
import { Typography } from "@mui/material";
import TimeDateAgo from "../features/TimeDateAgo";
import UserNameLink from "../../components/features/UserNameLink";

export default function PostList({ post }) {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);

  const { comments } = useSelector((state) => state.comments);

  const commentsInitialState = comments.map((obj) => ({
    ...obj,
    isEditing: false,
  }));

  const [commentsItem, setCommentsItem] = useState(commentsInitialState);

  let commentNum = 0;

  comments.map((comment) => post._id === comment.postId && commentNum++);

  useEffect(() => {
    dispatch(getComments());

    setCommentsItem(post.comments);
  }, [dispatch, JSON.stringify(comments)]);

  // Expand comments
  const [expanded, setExpanded] = React.useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  // Update isEditing state
  const handleEditComment = (commentId) => {
    setCommentsItem(
      commentsItem.map((data) => {
        return data._id === commentId
          ? { ...data, isEditing: !data.isEditing }
          : { ...data, isEditing: false };
      })
    );
  };

  // Like functions
  const [likesModal, setLikesModal] = React.useState(false);

  const openLikesModal = () => {
    //setLikesModal(true);
  };

  const closeLikesModal = () => {
    setLikesModal(false);
  };

  const handleLikeClick = (postId) => {
    var likeData = {
      userId: user.id,
      postId: postId,
    };

    dispatch(likePost(likeData));
  };

  let postLikes = 0;
  var likeButton;

  if (post.likes) {
    postLikes = post.likes.length;

    if (post.likes.some((id) => id === user.id)) {
      likeButton = (
        <Button
          variant="text"
          sx={{ textTransform: "capitalize" }}
          startIcon={<ThumbUpIcon />}
          onClick={() => handleLikeClick(post.id)}
          fullWidth
        >
          Liked
        </Button>
      );
    } else {
      likeButton = (
        <Button
          variant="text"
          sx={{ textTransform: "capitalize" }}
          startIcon={<ThumbUpOutlinedIcon />}
          onClick={() => handleLikeClick(post.id)}
          color="inherit"
          fullWidth
        >
          Like
        </Button>
      );
    }
  }

  var audienceIcon;

  if (post.audience === "Friends") {
    audienceIcon = (
      <Tooltip title={post.audience} placement="right">
        <PeopleAltIcon sx={{ fontSize: "1.10rem" }} />
      </Tooltip>
    );
  } else {
    audienceIcon = (
      <Tooltip title={post.audience} placement="right">
        <PublicIcon sx={{ fontSize: "1.10rem" }} />
      </Tooltip>
    );
  }
  return (
    <Grid item xs={12}>
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
            <Avatar
              src={post.userData.photo && `/uploads/${post.userData.photo}`}
              aria-label="avatar"
            />
          }
          action={<MenuItems componentType="post" componentData={post} />}
          title={<UserNameLink data={post.userData} />}
          subheader={
            <Stack direction="row" spacing={1} sx={{ mt: 0.4 }}>
              <TimeDateAgo timeDate={post.createdAt} />
              {audienceIcon}
            </Stack>
          }
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
        {(postLikes > 0 || commentNum > 0) && (
          <>
            <CardActions sx={{ pt: 1.3, pb: 1.3 }} disableSpacing>
              {postLikes > 0 && (
                <Stack direction="row" spacing={1}>
                  <RecommendIcon
                    color="primary"
                    onClick={openLikesModal}
                    fontSize="small"
                    sx={{ cursor: "pointer" }}
                  />
                  <Typography
                    sx={{ color: "#808080", cursor: "pointer" }}
                    onClick={openLikesModal}
                    variant="body2"
                  >
                    {postLikes}
                  </Typography>
                </Stack>
              )}
              {commentNum > 0 && (
                <Typography
                  sx={{ color: "#808080", marginLeft: "auto", mr: 1 }}
                  variant="body2"
                >
                  {commentNum} Comments
                </Typography>
              )}
              <LikesModal
                likesModal={likesModal}
                closeLikesModal={closeLikesModal}
                postUserId={post.user}
                likesUserId={post.likes.userId}
              />
            </CardActions>
          </>
        )}
        {(!post.photo || (post.photo && postLikes > 0) || commentNum > 0) && (
          <Divider variant="middle" />
        )}
        <CardActions disableSpacing>
          <Box sx={{ flexGrow: 1 }}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                {likeButton}
              </Grid>
              <Grid item xs={6}>
                <Button
                  variant="text"
                  sx={{ textTransform: "capitalize" }}
                  startIcon={<ChatBubbleOutlineOutlinedIcon />}
                  onClick={handleExpandClick}
                  color="inherit"
                  fullWidth
                >
                  Comments
                </Button>
              </Grid>
            </Grid>
          </Box>
        </CardActions>
        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <Divider variant="middle" />
          {commentsItem.map(
            (commentItem) =>
              post._id === commentItem.postId && (
                <CommentList
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
