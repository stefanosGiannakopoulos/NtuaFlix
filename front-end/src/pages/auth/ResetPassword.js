import React, { useState } from 'react'
import { useParams } from 'react-router-dom'
import axiosInstance from '../../api/api';

export default function ResetPassword() {

    const {secretToken} = useParams();
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState(null);
    const [msg, setMsg] = useState(null);

    async function submit(e) {
        e.preventDefault();
        setError(null);
        setMsg(null);
        const payload = {
            new_password: password,
            confirm_password: confirmPassword,
            secret_token: secretToken,
        }
        try{
            const response = await axiosInstance.post(`/reset-password/`, payload)
            if (response?.data?.err)
                setError(response?.data?.msg);
            else
                setMsg(response?.data?.msg);
        } catch (error) {
            setError(error?.response?.data?.detail)
        }
    }


  return (
    <div className='form-wrapper'>
    <form onSubmit={submit}>
    <h1 className='title-with-line'>Reset Password</h1>

        <div className='form-input'>
            <input type='password' placeholder='New Password' required value={password} onChange={(e) => setPassword(e.target.value)}/>
        </div>

        <div className='form-input'>
            <input type='password' placeholder='Confirm Password' required value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)}/>
        </div>
        
        <button type='submit' className='btn btn-primary btn-w100'>Reset Password</button>
        
        <p className='form-error'>{error}</p>
        <p className='form-success'>{msg}</p>
        
    </form>
</div>
  )
}
