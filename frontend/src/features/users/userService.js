import axios from 'axios'

// Get user data
const getUserDataById = async (userId) => {
    
    var response = await axios.get('/api/user/' + userId)
    return response.data
  }

const userService = {
  getUserDataById,
}

export default userService