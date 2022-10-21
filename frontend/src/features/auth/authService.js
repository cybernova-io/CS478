import axios from "axios";

const API_URL = "http://localhost:5000/api/";

// Register User
const register = async (userData) => {
  const response = await axios.post(API_URL, userData);

  if (response.data) {
    localStorage.setItem("user", JSON.stringify(response));
  }

  return response.data;
};

// Login User
const login = async (userData) => {
  const response = await axios.post("/login", userData);

  if (response.data) {
    localStorage.setItem("user", JSON.stringify(response));
  }

  return response.data;
};

// Logout User
const logout = () => {
  localStorage.removeItem("user");
};

const authService = {
  register,
  login,
  logout,
};

export default authService;
