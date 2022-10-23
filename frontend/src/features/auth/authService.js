import axios from "axios";

//const API_URL = "http://localhost:5000/api/";

// Get user data
const getMe = async (token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }

  const response = await axios.get(API_URL + 'me', config)

  return response.data
}
// Register User
const register = async (userData) => {
  const response = await axios.post(API_URL, userData);

  if (response.data) {
    localStorage.setItem("user", JSON.stringify(response));
    localStorage.setItem('isDarkMode', JSON.stringify(response.data.settings.isDarkMode))          
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

// Update post
const updateUserSettings = async (userData, token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }

  const response = await axios.put(API_URL + 'settings', userData, config)

  return response.data
}


const authService = {
  getMe,
  register,
  login,
  logout,
  updateUserSettings
};

export default authService;
