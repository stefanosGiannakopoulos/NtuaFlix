import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import axiosInstance from '../../api/api';
import  AuthContext  from '../../context/AuthContext';
import {useContext} from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
    const navigate = useNavigate();

    const {saveTokens} = useContext(AuthContext);
    
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    async function submit(e) {
        e.preventDefault();
        setError('');
        setLoading(true);


        const payload = {
            username: username,
            password: password,
        }
        setPassword('');

        try{
            const response = await axiosInstance.post(`/login`, payload, {
                headers: {'content-type': 'application/x-www-form-urlencoded'}});
            
            saveTokens(response?.data?.token);
            navigate('/', {replace:true})
        }
        catch (error) {
            setError(error?.response?.data?.detail)
        }
    }


  return (
    <div className='form-wrapper'>
        <form onSubmit={submit}>
        <h1 className='title-with-line'>Sign in</h1>

            <div className='form-input'>
                <input type='text' placeholder='Username' required autoCapitalize={false} value={username} onChange={(e) => setUsername(e.target.value)}/>
            </div>
            
            <div className='form-input'>
                <input type='password' placeholder='Password' required value={password} onChange={(e) => setPassword(e.target.value)}/>
            </div>

            <button type='submit' className='btn btn-primary btn-w100'>Sign in</button>
            
            <p className='form-error'>{error}</p>
            
            <div className='alternative-link'>
                <p>Don't have an account yet? Sign up <Link to='/auth/register'>here</Link>.</p>
            </div>
            <div className='alternative-link'>
                <p>Forgot your password? Reset it <Link to='/auth/forgot-password'>here</Link>.</p>
            </div>
        </form>
    </div>
  )
}
