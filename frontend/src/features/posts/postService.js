import axios from "axios";

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
  
  const response = await axios.get('/api/feed')
        .then((response) => {
          return response;
        })
        .catch(function (error) {
          console.log(error);
        });;
        
  return response;

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
}

// Like post
const likePost = async (postId, postData, token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }

  const response = await axios.put(API_URL + postId + '/likes', postData, config)

  return response.data
}

const postService = {
  createPost,
  getPosts,
  deletePost,
  likePost,
};

export default postService;

