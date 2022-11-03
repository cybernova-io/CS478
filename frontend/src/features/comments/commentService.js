import axios from "axios";

const API_URL = "http://localhost:5000/api/comments/";

// Create new comment
const createComment = async (commentData, token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const response = await axios.post(API_URL, commentData, config);

  return response.data;
};

// Get user comments
const getComments = async (token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const response = await axios.get(API_URL, config);

  return response.data;
};

// Update comment
const updateComment = async (commentId, commentData, token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const response = await axios.put(API_URL + commentId, commentData, config);

  return response.data;
};

// Delete user comment
const deleteComment = async (commentId, token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const response = await axios.delete(API_URL + commentId, config);

  return response.data;
};

// Like comment
const likeComment = async (commentId, commentData, token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }

  const response = await axios.put(API_URL + commentId + '/likes', commentData, config)

  return response.data
}


const commentService = {
  createComment,
  getComments,
  updateComment,
  deleteComment,
  likeComment,
};

export default commentService;
