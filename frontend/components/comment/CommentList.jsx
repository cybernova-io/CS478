import * as React from "react";
import { useState, useEffect } from "react";
import Avatar from "@mui/material/Avatar";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import { useDispatch, useSelector } from "react-redux";
import TextField from "@mui/material/TextField";
import { updateComment } from "../../src/features/comments/commentSlice";
import ReadMore from "../features/Readmore";
import Box from "@mui/material/Box";
import { toast } from "react-toastify";
import MenuItems from "../features/MenuItems";
import { likeComment } from "../../src/features/comments/commentSlice";
import Badge from "@mui/material/Badge";
import RecommendIcon from "@mui/icons-material/Recommend";
import { styled } from "@mui/material/styles";
import LikesModal from "../like/LikesModal";
import TimeDateAgo from "../features/TimeDateAgo";
import UserNameLink from "../../components/features/UserNameLink";

const CustomizedBadge = styled(Badge)`
  .MuiBadge-badge {
    bottom: 15px;
    right: -11px;
  }
`;

export default function CommentList(props) {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  let commentLikes = 0;

  // Comment form
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

  // Menu
  const handleEditMenu = (commentId) => {
    // setAnchorEl(null);
    return props.handleEditComment(commentId);
  };

  // Like functions
  const [likesModal, setLikesModal] = React.useState(false);

  const openLikesModal = () => {
    setLikesModal(true);
  };

  const closeLikesModal = () => {
    setLikesModal(false);
  };

  // Like button
  const handleLikeClick = (commentId) => {
    var likeData = {
      userId: user._id,
      commentId: commentId,
    };

    dispatch(likeComment(likeData));
  };

  var likeButton;

  commentLikes = props.commentData.likes.userId.length;

  if (props.commentData.likes) {
    commentLikes = props.commentData.likes.userId.length;

    if (props.commentData.likes.userId.some((id) => id === user._id)) {
      likeButton = (
        <Typography
          variant="caption"
          sx={{ p: 1.3, fontWeight: "bold", cursor: "pointer" }}
          color="primary"
          onClick={() => handleLikeClick(props.commentData._id)}
        >
          Liked
        </Typography>
      );
    } else {
      likeButton = (
        <Typography
          variant="caption"
          sx={{ p: 1.3, fontWeight: "bold", cursor: "pointer" }}
          color="text.secondary"
          onClick={() => handleLikeClick(props.commentData._id)}
        >
          Like
        </Typography>
      );
    }
  }

  return (
    <Grid container wrap="nowrap" spacing={2} sx={{ p: 2 }}>
      <Grid item>
        <Avatar
          src={
            props.commentData.userData.photo &&
            `/uploads/${props.commentData.userData.photo}`
          }
          aria-label="avatar"
        />
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
          <Typography variant="caption" sx={{ p: 1.3 }} color="text.secondary">
            Press Enter to save.
          </Typography>
        </Grid>
      ) : (
        <>
          <Grid justifyContent="left" item>
            <CustomizedBadge
              badgeContent={
                <Box
                  sx={{
                    backgroundColor: (theme) =>
                      theme.palette.mode === "light"
                        ? theme.palette.grey[200]
                        : theme.palette.grey[800],
                    borderRadius: 5,
                    width: "max-content",
                    display: "flex",
                    alignItems: "center",
                    cursor: "pointer",
                  }}
                  onClick={openLikesModal}
                >
                  <RecommendIcon color="primary" fontSize="small" />
                  <Typography
                    variant="body 2"
                    color="text.secondary"
                    sx={{ ml: 0.5, mr: 0.9 }}
                  >
                    {commentLikes}
                  </Typography>
                </Box>
              }
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "right",
              }}
              invisible={commentLikes > 0 ? false : true}
            >
              <Box
                sx={{
                  backgroundColor: (theme) =>
                    theme.palette.mode === "light"
                      ? theme.palette.grey[200]
                      : theme.palette.grey[800],
                  p: 1,
                  borderRadius: 5,
                  width: "max-content",
                  maxWidth: 575,
                  whiteSpace: "pre-wrap",
                  wordWrap: "break-word",
                }}
              >
                <UserNameLink data={props.commentData.userData} />
                <ReadMore>{props.commentData.comment}</ReadMore>
              </Box>
            </CustomizedBadge>
            <br />
            {likeButton}
            <Typography variant="caption" color="text.secondary">
              <TimeDateAgo timeDate={props.commentData.createdAt} />
            </Typography>
            <LikesModal
              likesModal={likesModal}
              closeLikesModal={closeLikesModal}
              likesUserId={props.commentData.likes.userId}
            />
          </Grid>
          <Grid item>
            <Box sx={{ float: "left" }}>
              {props.commentData.user === user._id && (
                <MenuItems
                  componentType="comment"
                  componentData={props.commentData}
                  componentFunc={handleEditMenu}
                />
              )}
            </Box>
          </Grid>
        </>
      )}
    </Grid>
  );
}
