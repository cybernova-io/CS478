import axios from 'axios';

class SignUpDataService {

    post(data) {
        return axios.post("/signup", data)
    }

}

export default new SignUpDataService();