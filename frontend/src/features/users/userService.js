import axios from "axios";

const API_URL = "/api/users/";

const config = (token) => {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
};

// Get user data
const getUserDataById = async (userId, token) => {
  var response = await axios.get(API_URL + userId, config(token));

  return response.data;
};

const userService = { getUserDataById };

export default userService;
