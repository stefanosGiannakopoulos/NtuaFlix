import React, { useState } from 'react'
import axiosInstance from '../../api/api';

export default function ForgotPassword() {

    const [email, setEmail] = useState('');
    const [error, setError] = useState(null);
    const [msg, setMsg] = useState();

    async function submit(e) {
        e.preventDefault();
        setError(false);
        setMsg(false);
        
        try{
            const response = await axiosInstance.get(`/forget-password?email=${email}`);
            if (response?.data?.err)
                setError(response?.data?.msg);
            else
                setMsg(response?.data?.msg);
        } catch(error) {
            setError(error?.response?.data?.detail)
        }

    }

  return (
    <div className='form-wrapper'>
        <form onSubmit={submit}>
        <h1 className='title-with-line'>Forgot Password</h1>
        <div className='alternative-link'>
                <p>
                    Looks like you forgot your password. A link will be sent to your email. Please check your spam!
                </p>
            </div>

            <div className='form-input'>
                <input type='email' placeholder='Email' required value={email} onChange={(e) => setEmail(e.target.value)}/>
            </div>
            

            <button type='submit' className='btn btn-primary btn-w100'>Send Email</button>
            
            <p className='form-error'>{error}</p>
            <p className='form-success'>{msg}</p>
            
        </form>
    </div>
  )
}
