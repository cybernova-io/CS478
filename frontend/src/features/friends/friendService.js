import axios from "axios";

const API_URL = "/api/friends/";

const config = (token) => {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
};

// Get user friends
const getUserFriends = async (token) => {
  const response = await axios.get(API_URL, config(token));

  return response.data;
};

// Get friends data
const getFriendsDataById = async (friendsId, token) => {
  const response = await axios.get(
    API_URL + "friend/" + friendsId,
    config(token)
  );

  return response.data;
};

// Get all friends
const getAllFriends = async (token) => {
  const response = await axios.get(API_URL + "allfriends/", config(token));

  return response.data;
};

// Get all friends
const getAllFriendsById = async (userId, token) => {
  const response = await axios.get(
    API_URL + "allfriends/" + userId,
    config(token)
  );

  return response.data;
};

// Get friends suggestions
const getFriendSuggestions = async (token) => {
  const response = await axios.get(API_URL + "suggestions/", config(token));

  return response.data;
};

// Send friend Request
const sendFriendRequest = async (friendRequestData, token) => {
  const response = await axios.post(
    API_URL + "request/",
    friendRequestData,
    config(token)
  );

  return response.data;
};

// Cancel or reject friend request
const rejectFriendRequest = async (friendRequestData, token) => {
  const response = await axios.put(
    API_URL + "reject/",
    friendRequestData,
    config(token)
  );

  return response.data;
};

// Cancel or reject friend request
const unFriend = async (friendRequestData, token) => {
  const response = await axios.put(
    API_URL + "unfriend/",
    friendRequestData,
    config(token)
  );

  return response.data;
};

// Accept friend request
const acceptFriendRequest = async (friendRequestData, token) => {
  const response = await axios.put(
    API_URL + "accept/",
    friendRequestData,
    config(token)
  );

  return response.data;
};

const friendService = {
  getUserFriends,
  getAllFriendsById,
  getFriendsDataById,
  getAllFriends,
  getFriendSuggestions,
  sendFriendRequest,
  rejectFriendRequest,
  unFriend,
  acceptFriendRequest,
};

export default friendService;
