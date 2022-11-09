import axios from "axios";

const API_URL = "http://localhost:5000/api/users/";

const config = (token) => {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
};

// Get user data
const getMe = async (token) => {
  const response = await axios.get(API_URL + "me", config);

  return response.data;
};
// Register User
const register = async (userData) => {
  const response = await axios.post(API_URL, userData);

  if (response.data) {
    localStorage.setItem("user", JSON.stringify(response.data));
  }

  return response.data;
};

// Update user
const updateUser = async (userData, token) => {
  const response = await axios.put(
    API_URL + "account",
    userData,
    config(token)
  );

  return response.data;
};

// Login User
const login = async (userData) => {
  const response = await axios.post(API_URL + "login", userData);
  if (response.data) {
    localStorage.setItem("user", JSON.stringify(response.data));
    localStorage.setItem(
      "isDarkMode",
      JSON.stringify(response.data.settings.isDarkMode)
    );
  }

  return response.data;
};

// Logout User
const logout = () => {
  localStorage.removeItem("user");
  localStorage.removeItem("isDarkMode");
};

// Update settings
const updateUserSettings = async (userData, token) => {
  const response = await axios.put(
    API_URL + "settings",
    userData,
    config(token)
  );
  return response.data;
};

const authService = {
  getMe,
  register,
  updateUser,
  login,
  logout,
  updateUserSettings,
};

export default authService;
