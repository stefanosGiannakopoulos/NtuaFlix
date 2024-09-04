import React, {useEffect} from 'react'
import './NotRegistered.css'
import { Link } from 'react-router-dom'
import { useLocation } from 'react-router-dom';


export default function NotRegistered() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return (
    <div className='not-registered-background'>
        <div className='not-registered-container'>
            <h1 className='h2 title-with-line'>You must be registered</h1>
            <div className='message-description'>
                <p>In order to access your WatchList you must have a <mark>NtuaFlix account</mark>.</p>
                <p>Please Sign Up <Link to='/auth/register' className='a-transition'>here</Link> if you don't have a NtuaFlix account or Sign In <Link to='/auth/login/' className='a-transition'>here</Link>.</p>
            </div>
        </div>
    </div>
  )
}
