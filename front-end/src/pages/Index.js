import React, { useEffect, useState } from 'react'
import MovieCard from '../components/MovieCard'
import Hero from '../components/Hero'
import axiosInstance from '../api/api'
import Preloader from '../components/Preloader'
import { Link, useLocation } from 'react-router-dom'
import './Index.css'

export default function Index() {
  const { pathname } = useLocation();


    const [loading, setLoading] = useState(true);
    const [data, setData] = useState(null);

    async function fetchMovieData() {
      const response = await axiosInstance.get('/index-movies');
      

      setData(response?.data);
      console.log(response?.data)
      setLoading(false);

      for(let i =0; i < response?.data.length; ++i) {
        setTimeout(() => initiateHorizontalScroll(response?.data[i].genre), 2000);
      }
    }

    useEffect( () => {
      fetchMovieData();
    }, [])

    useEffect(() => {
      window.scrollTo(0, 0);
    }, [pathname]);

    function initiateHorizontalScroll(genre) {
      try {
        const cardContainer = document.getElementById(`${genre}-container`);
        const cards = cardContainer.querySelectorAll('.card');
        const cardWidth = cards[0].offsetWidth; // Width of a card plus margin

        let scrollPosition = 0;



      function scrollCards() {

        scrollPosition += 0.5;
        cardContainer.scrollLeft = scrollPosition;

        if (scrollPosition >= cardWidth * cards.length - cardContainer.offsetWidth + 100) {
          scrollPosition = 0;
        }


        requestAnimationFrame(scrollCards);
      }

      // Start scrolling on page load
        scrollCards();
    } catch(error)  {
      console.log(error);
    }
    
    }
    
  if(loading) return <Preloader />

  return (
    <>
        <Hero />

        {data && data.map((genre) => { return genre.movies.length > 0 && <div>
           <div className='section-title-container section-index'>
               <h2 className='h2 title-with-line'>{genre.genre}</h2>
               <Link to={`/movies?genre=${genre.genre_id}`} className='view-more-link'>View More</Link>
           </div>
           <div className='cards-container' id={`${genre.genre}-container`}>
               {genre.movies.map((movie) => {
                return <MovieCard key={movie.tconst} movieID={movie.tconst} movieTitle={movie.primary_title} 
                averageRating={movie.average_rating} 
                imageUrl={movie.image_url} />
               })}
           </div>
       </div>
        })}
    </>
  )
}
