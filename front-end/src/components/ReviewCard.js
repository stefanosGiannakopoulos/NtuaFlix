import React from 'react'
import './ReviewCard.css'
import { Link } from 'react-router-dom'
import StarBorderIcon from '@mui/icons-material/StarBorder';
import StarIcon from '@mui/icons-material/Star';
import { AiFillLike, AiFillDislike } from "react-icons/ai";
import axiosInstance from '../api/api';
import AuthContext from '../context/AuthContext'
import { useContext, useEffect, useState } from 'react'


export default function ReviewCard({id, username, title, stars, text, likes, dislikes, date, fetchReviews, myreviews}) {

    const { user } = useContext(AuthContext);
    const { authTokens } = useContext(AuthContext);

    console.log(myreviews)

    const [liked, setLiked] = useState(false);
    const [disliked, setDisliked] = useState(false);

    const starIcons = [];
    for (let i = 0; i < 5; ++i) {
        if (i < stars) {
            starIcons.push(<StarIcon key={i} />);
        } else {
            starIcons.push(<StarBorderIcon key={i} />);
        }
    }

    // const [updatedLikes, setUpdatedLikes] = useState(likes);
    // const [updatedDislikes, setUpdatedDislikes] = useState(dislikes);


    const handleReaction = async(type) => {
        try {
            const response = await axiosInstance.post(`/reviews/${id}/${user.user_id}?like=${type}` ,null,{
                headers: {
                  'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`,
                },
              });
              if (response.status===200){
                setLiked(type);
                setDisliked(type);
                fetchReviews();
            }
        }
        catch(error){
            console.log(error);
        } 
    }

    const deleteReview = async () => {
        try {
            const response = await axiosInstance.delete(`/myreviews/${user.user_id}/remove?review_id=${id}` ,{
                headers: {
                  'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`,
                },
              });
              if (response.status===200){
                console.log("review deleted");
                fetchReviews();
            }
        }
        catch(error){
            console.log(error);
        } 
    }

useEffect(()=>{
    const userReaction = async () => {
        try{
            const response = await axiosInstance.get(`/reviews/reactions?user_id=${user.user_id}&review_id=${id}`, {
                headers: {
                    'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`,
                  },
            });
            setLiked(response?.data.like);
            setDisliked(response?.data.dislike);
        } catch(error){
            console.log(error);
        }
    }
    userReaction();
},[user, authTokens]);


    return (
        <div className='review-card'>
        <div className='user-info'>
            <div className='user-avatar'/>
            <span className='user-name'>{username}</span>
            <span className="date">{date}</span>
        </div>
        <span className='movie-title'>{title}</span>
        <div className="review-stars">
                {starIcons.map((icon, index) => (
                    <span key={index}>{icon}</span>
                ))}
            </div>
        <p className="review-text">
            "{text}"
        </p>
        <div className="review-actions">
            <span>Likes:{likes}  </span>
            <button className={`like-button ${liked ? 'liked' : ''}`}
            onClick={() => {
            setLiked(!liked);
            handleReaction(true);
            }}><AiFillLike /></button>

            <span>Dislikes:{dislikes}  </span>
            <button className={`dislike-button ${disliked ? 'disliked' : ''}`}
            onClick={() => {
            setDisliked(!disliked);
            handleReaction(false);
            }}><AiFillDislike /></button>
        </div>
        {myreviews && 
            <button className='dlt-btn' onClick={()=>deleteReview()}>delete</button>
            }
    </div>
    )
}