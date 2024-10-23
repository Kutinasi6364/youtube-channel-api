import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    interface LoginResponse {
        access: string;
        refresh: string;
    }

    const handleSubmit = async (e: React.SyntheticEvent) => {
        e.preventDefault();
        try {
            const response = await axios.post<LoginResponse>('http://localhost:8000/accounts/api/login/', {
                username,
                password,
            });
            console.log(response.data);  // トークンが返ってきたか確認
            const { access, refresh } = response.data;  // トークンを取得
            localStorage.setItem('access_token', access);  // トークンを保存
            localStorage.setItem('refresh_token', refresh);
            navigate('/');
        } catch (error) {
            console.error('Login failed', error);
        }
    };

    return (
        <div className="d-flex justify-content-center">
            <div className="card shadow-sm mt-5 p-5 w-50">
                <h3 className="text-center">Login</h3>
                <form onSubmit={handleSubmit}  className="p-4 m-4 bg-light border border-success d-flex flex-column align-items-center ">
                    <div className="mb-3 w-50">
                        <input 
                            className="form-control"
                            type="text" 
                            placeholder="Username" 
                            value={username} 
                            onChange={(e) => setUsername(e.target.value)} 
                        />
                    </div>
                    <div className="mb-3 w-50">
                        <input 
                            className="form-control"
                            type="password" 
                            placeholder="Password" 
                            value={password} 
                            onChange={(e) => setPassword(e.target.value)} 
                        />
                    </div>
                    <div className="b-grid d-flex justify-content-center">
                        <button type="submit" className="btn btn-success">Login</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;
