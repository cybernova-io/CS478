import axios from "axios";

const API_URL = "http://localhost:5000/api/posts/";

const config = (token) => {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
};
// Create new post
const createPost = async (postData, token) => {
  const response = await axios.post(API_URL, postData, config(token));
  return response.data;
};

// Get user posts
const getPosts = async (token) => {
  const response = await axios.get(API_URL, config(token));
  return response.data;
};

// Update post
const updatePost = async (postId, postData, token) => {
  const response = await axios.put(API_URL + postId, postData, config(token));
  return response.data;
};

// Delete user post
const deletePost = async (postId, token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    data: {
      fileName: postPhoto,
    },
  };

  const response = await axios.delete(API_URL + postId, config);
  return response.data;
};

// Like post
const likePost = async (postId, postData, token) => {
  const response = await axios.put(
    API_URL + postId + "/likes",
    postData,
    config(token)
  );

  return response.data;
};

// Save post
const savePost = async (postId, postData, token) => {
  const response = await axios.put(
    API_URL + postId + "/saves",
    postData,
    config(token)
  );
  return response.data;
};

const postService = {
  createPost,
  getPosts,
  updatePost,
  deletePost,
  likePost,
  savePost,
};

export default postService;
