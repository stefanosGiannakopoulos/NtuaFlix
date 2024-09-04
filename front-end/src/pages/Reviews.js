import React from 'react'
import './Reviews.css'
import AuthContext from '../context/AuthContext'
import { useContext, useEffect, useState } from 'react'
import axiosInstance from '../api/api'
import { Link } from 'react-router-dom';
import ReviewCard from '../components/ReviewCard';
import { useLocation } from 'react-router-dom';
import axios from 'axios'


export default function Reviews() {
  const { pathname } = useLocation();

    const { user } = useContext(AuthContext);
    const { authTokens } = useContext(AuthContext);

    const [userOnly, setUserOnly] = useState(false);
    const [reviews, setReviews] = useState([]);

    const [searchQuery, setSearchQuery] = useState('');
    const [filteredReviews, setFilteredReviews] = useState(reviews);


    const fetchReviews = async () => {
      setReviews([])
        try {
          let endpoint = '/reviews';
          if (userOnly) {
            endpoint = `/myreviews/${user.user_id}`;
          }
  
          const response = await axiosInstance.get(endpoint, {
            headers: {
              'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`,
            },
          });
  
          if (response.status === 200) {
            const sortedReviews = response.data.sort((a, b) => {
              if (a.upload !== b.upload) {
                return (a.upload) - (b.upload);
              } else {
                return a.id - b.id;
              }
            });
            setReviews(sortedReviews);
            console.log(reviews);
          }
        } catch (error) {
          console.error('Error fetching reviews:', error);
        }
      };


    useEffect(() => {    
        fetchReviews();
      }, [user?.user_id, authTokens, userOnly]);

      useEffect(() => {
        window.scrollTo(0, 0);
      }, [pathname]);

      useEffect(() => {
        const filtered = reviews.filter(review =>
          review.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
          review.title.toLowerCase().includes(searchQuery.toLowerCase())
        );
        setFilteredReviews(filtered);
      }, [searchQuery, reviews]);

      const handleSearchChange = (e) => {
        setSearchQuery(e.target.value);
        console.log(searchQuery);
      };

    return (
        <div className='theme'>
            <nav className='reviews-navbar'>
                <Link to={'/reviews/'} onClick={ () => setUserOnly(false) }>All Reviews</Link>
                <Link to={'/reviews/'} onClick={ () => setUserOnly(true)}>My Reviews</Link>
                <Link to={'/makereview/'}>Make Review</Link>
            </nav>

            {!userOnly &&
            <div className='filter-reviews'>
            <input
              type="text"
              placeholder="Search reviews by username / movie title..."
              value={searchQuery}
              onChange={handleSearchChange}
            />
            </div>
            }

            <div>
            {filteredReviews && filteredReviews.map((review) => {
            return <ReviewCard
              key={review.id}
              id = {review.id}
              username={review.username} 
              title={review.title} 
              stars={review.stars} 
              likes={review.likes}
              dislikes = {review.dislikes}
              text = {review.text}
              date = {review.uploaded}
              fetchReviews = {fetchReviews} 
              myreviews={review.username === user.username}
            />
        })}
            </div>
        </div>
    )
}