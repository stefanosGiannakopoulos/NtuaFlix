import React from 'react'
import './MakeReview.css'
import AuthContext from '../context/AuthContext'
import { useContext, useEffect, useState } from 'react'
import NotRegistered from './NotRegistered';
import axiosInstance from '../api/api'
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useLocation } from 'react-router-dom';

export default function NewReview (props) {
    const { pathname } = useLocation();
    const [searchParams] = useSearchParams();
    const [revtitle, setRevtitle] = useState('');

    useEffect(() => {
        const revtitleParam = searchParams.get('revtitle');
        if (revtitleParam) {
            setRevtitle(revtitleParam);
            setTitle(revtitleParam); //Auto-fills first input in the form
        }
      }, [searchParams]);

    const navigate = useNavigate();
    const gotomovies = () => {
        navigate('/movies');
    }

    const gotomyreviews = () => {
        navigate('/reviews/');
    }

    const {user} = useContext(AuthContext);
    const { authTokens } = useContext(AuthContext);

    const [title, setTitle] = useState('');
    const [review_text, setReviewText] = useState('');
    const [rating, setRating] = useState(0);
    const [flashMessage, setFlashMessage] = useState('');

    async function make_review (e) {
        e.preventDefault();
        try {
            const response = await axiosInstance.post(
                `/myreviews/${user.user_id}/add?movie_title=${title}&text=${review_text}&stars=${rating}`, null,
                {
                    headers: {
                        'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`,
                        'Content-Type': 'application/json',
                    },
                }
            );
            console.log(response);
            if (response.status === 200) {
                console.log(response.data.message);
                gotomyreviews();
            }
        } catch (error) {
            console.error('Error uploading review:');
            console.log('Validation Errors:', error.response.data);
            if (error.response && error.response.status === 404) {
                setFlashMessage('Movie not found. Please check the title.');
              } else {
                setFlashMessage('An error occurred. Please try again.');
              }
        }
        setRating(0);
        setReviewText('');
        setTitle(''); 

}

    const handleStarClick = (value) => {
        setRating(value);
      };

      useEffect(() => {
        window.scrollTo(0, 0);
      }, [pathname]);

    return (
        <div className='page-container'>
        <h1 className='review-header'>Make your review here!</h1>
        <div className='review-form-container'>
            <form className = "review-form" onSubmit = {make_review} >
            <label for="title">Movie Title</label>
            <input value = {title} onChange = {(e) => setTitle(e.target.value)} 
             type="text" placeholder={revtitle? revtitle : "Enter Original Title"} id="title" name="title" required/>

                <label>Your Rating: {rating}</label>
                <div className="stars-container">
                {[1, 2, 3, 4, 5].map((value) => (
                    <span
                    key={value}
                    className={`star ${value <= rating ? 'filled' : ''}`}
                    onClick={() => handleStarClick(value)}
                    >
                    ★
                    </span>
                ))}
                </div>

            <label htmlFor='text'>Add Text</label>
            <input value = {review_text} onChange = {(e) => setReviewText(e.target.value)} 
            type="text" placeholder="..." id="text" name="text" />
            <button type ="submit">Upload</button>
        </form>

        {flashMessage && (
        <div className="flash-message">
          {flashMessage}
          <button className= 'error-btn' onClick={() => setFlashMessage('')}>Close</button>
        </div>
      )}
        </div>
        <button className = 'link-btn' onClick={gotomovies}>Not sure? Browse Movies</button>
        </div>
    )
}