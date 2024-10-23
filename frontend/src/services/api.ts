import axios from 'axios';

// Django API ベースURL
const API_BASE_URL = 'http://localhost:8000/channels/api/';

export const getChannels = () => {
    const access_token = localStorage.getItem('access_token');
    console.log("token: " + access_token);
    if (!access_token) {
        throw new Error('Token not found');
    }
    return axios.get(`${API_BASE_URL}channel_list/`, {
        headers: {
            Authorization: `Bearer ${access_token}` // ユーザー情報を渡す
        }
    })
}