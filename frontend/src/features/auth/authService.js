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
  
  const response = await axios.post('/api/signup', userData)
  .then(function (response) {
    //console.log(response.data);
    if (response.data) {
      localStorage.setItem("user", JSON.stringify(response));
      //localStorage.setItem('isDarkMode', JSON.stringify(response.data.settings.isDarkMode))          
    }

    return response
  })
  .catch(function (error) {
    console.log(error);
  });

  return response;
};

// Login User
const login = async (userData) => {
  
  const response = await axios.post('/api/login', userData)
  .then(function (response) {
    //console.log(response.data);
    return response
  })
  .catch(function (error) {
    console.log(error);
  });

  if (response.data) {
    localStorage.setItem("user", JSON.stringify(response));
  }

  return response
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
