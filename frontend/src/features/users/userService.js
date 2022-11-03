import axios from 'axios'

const API_URL = 'http://localhost:5000/api/users/'

// Get user data
const getUserDataById = async (userId, token) => {
    const config = {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    } 

    var response = await axios.get(API_URL + 'user/' + userId, config)

    return response.data
  }

const userService = {
  getUserDataById,
}

export default userService