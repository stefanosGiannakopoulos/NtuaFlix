import React, { useContext, useEffect, useState } from 'react'
import AuthContext from '../context/AuthContext'
import NotRegistered from './NotRegistered';
import './Statistics.css';
import { Link } from 'react-router-dom';
import Preloader from '../components/Preloader';
import { useLocation } from 'react-router-dom';


export default function Statistics() {
    const { pathname } = useLocation();

    const {authTokens} = useContext(AuthContext);

    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        setIsLoading(false);
    }, []);

    useEffect(() => {
        window.scrollTo(0, 0);
      }, [pathname]);

    if (!authTokens) return <NotRegistered />
    if (isLoading) return <Preloader /> 

    return (
        <div className='page-container'>
            <div>
                <h1 style={{marginBottom: 10, textAlign:'center', color: '#8d2481', fontSize: 65}}>
                    Statistics
                </h1>
                <div className='statistics-container'>
                        <div className='statistics-column'>
                            <div className='statistics-row'>
                                <h2 style={{marginBottom: 10, color: '#c37892'}}>Your Reviews Statistics</h2>
                                <Link to={`/account/statistics/reviews/`} className='view-more-link'>View More</Link>
                            </div>
                        </div>
                </div>
                <div className='statistics-container'>
                        <div className='statistics-column'>
                            <div className='statistics-row'>
                                <h2 style={{marginBottom: 10, color: '#c37892'}}>Your Watchlists Statistics</h2>
                                <Link to={`/account/statistics/watchlists/`} className='view-more-link'>View More</Link>
                            </div>
                        </div>
                </div>
            </div>
        </div>
    )

}