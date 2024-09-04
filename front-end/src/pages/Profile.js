import { useContext, useEffect, useState } from 'react'
import axiosInstance from '../api/api';
import { useNavigate } from "react-router-dom";
import './auth/Auth.css'
import React from 'react'
import { useLocation } from 'react-router-dom';
import  AuthContext  from '../context/AuthContext'
import Preloader from '../components/Preloader';
import NotRegistered from './NotRegistered';




export default function Profile() {
  const { pathname } = useLocation();

    const navigate = useNavigate();
    // Assuming AuthContext provides a state named authTokens
    const {authTokens} = useContext(AuthContext);

   /* const [userProfile, setUserProfile] = useState({
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        dob: '',
      });
*/
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [dob, setDob] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(true);


    const fetchUserProfile = async () => {
      try {
        const response = await axiosInstance.get(`/user-profile`, {
          headers: {
             'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`,
             'Content-Type': 'application/json'
          },
        });
        //setUserProfile(response.data);
        setUsername(response.data.username);
        setEmail(response.data.email);
        setFirstName(response.data.first_name);
        setLastName(response.data.last_name);
        setDob(response.data.dob);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching user profile:', error);
      }
    };

    useEffect(() => {
        
        fetchUserProfile(); 
      }, []); // The empty dependency array ensures that this effect runs only once, similar to componentDidMount
    

    async function submit(e) {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        const payload = {
            username: username,
            first_name: firstName,
            last_name: lastName,
            email: email,
            dob: dob,
        }


        try {
            const response = await axiosInstance.post(`/update-profile`, payload, { 
              headers: {
                 'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`,
                 'Content-Type': 'application/json'
              },
            });
            setSuccess('Profile updated successfully');
            //navigate('/', {replace:true})
        }
        catch (error) {
            setError(error?.response?.data?.detail)
        }
    }

    useEffect(() => {
      window.scrollTo(0, 0);
    }, [pathname]);

    if (loading) {
      return <Preloader/>;
    }

    if (!authTokens) return <NotRegistered />;
  return (
    <div className='auth-page'>
    <div className='auth-container'>

    <div className='form-wrapper'>
        <form onSubmit={submit}>
        <h1 className='title-with-line'>User Profile</h1>

            <div className='form-input'>
                <input type='text'  readOnly value={username} />
            </div>

              <div className='form-input'>
                  <input type='text' placeholder='First name' required value={firstName} onChange={(e) => setFirstName(e.target.value)}/>
              </div>

              <div className='form-input'>
                  <input type='text' placeholder='Last name' required value={lastName} onChange={(e) => setLastName(e.target.value)}/>
              </div>

              <div className='form-input'>
                  <input type='email' placeholder='Email' required value={email} onChange={(e) => setEmail(e.target.value)}/>
              </div>
              
              <div className='form-input'>
                  <input type="date" value={dob} onChange={(e) => setDob(e.target.value)} required />
              </div>


            <button type='submit' className='btn btn-primary btn-w100'>Update Profile</button>
            
            <p className='form-error'>{error}</p>
            <p className='form-success'>{success}</p>

        </form>
    </div>
    
    </div>
    </div>
  )
}
