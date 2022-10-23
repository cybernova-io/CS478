import axios from "axios";

const API_URL = "";

// Create new post
const createPost = async (postData, token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const response = await axios.post(API_URL, postData, config);

  return response.data;
};

// Get user posts
const getPosts = async () => {
  
  const response = await axios.get('/post');
  return response.data;
  
};

// Delete user post
const deletePost = async (postId, token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const response = await axios.delete(API_URL + postId, config);

  return response.data;
};

const postService = {
  createPost,
  getPosts,
  deletePost,
};

export default postService;
