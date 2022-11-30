import axios from "axios";

const API_URL = "/api/comments/";

const config = (token) => {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
};

// Create new comment
const createComment = async (commentData, token) => {
  const response = await axios.post(API_URL, commentData, config(token));

  return response.data;
};

// Get user comments
const getComments = async (token) => {
  const response = await axios.get(API_URL, config(token));

  return response.data;
};

// Update comment
const updateComment = async (commentId, commentData, token) => {
  const response = await axios.put(
    API_URL + commentId,
    commentData,
    config(token)
  );

  return response.data;
};

// Delete user comment
const deleteComment = async (commentId, token) => {
  const response = await axios.delete(API_URL + commentId, config(token));

  return response.data;
};

// Like comment
const likeComment = async (commentId, commentData, token) => {
  const response = await axios.put(
    API_URL + commentId + "/likes",
    commentData,
    config(token)
  );
  return response.data;
};

const commentService = {
  createComment,
  getComments,
  updateComment,
  deleteComment,
  likeComment,
};

export default commentService;
