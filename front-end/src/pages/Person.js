import React, { useEffect, useState } from 'react'
import './Person.css'
import { useParams } from 'react-router-dom'
import axiosInstance from '../api/api';
import Preloader from '../components/Preloader';
import MovieCard from '../components/MovieCard';
import { useLocation } from 'react-router-dom';
export default function Person() {
  const { pathname } = useLocation();

  const {personID} = useParams();
  const [personData, setPersonData] = useState(null);
  const [loading, setLoading] = useState(true);

  async function fetchPerson() {
    const response = await axiosInstance.get(`/name_whole/${personID}`);
    setPersonData(response?.data);
    setLoading(false);
  }

  useEffect( () => {
    fetchPerson();
  }, []) 

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  if (loading) return <Preloader />
  
  return (
    <div className='page-container'>
        <div className='movie-container'>
            <div className='movie-column'>
                    <div className='movie-row'>
                    
                        <p className='movie-genres'>{personData?.profession.map(obj => obj.name).join(', ')}</p>

                        <h1 className='title-with-line'>{personData?.primary_name}</h1>
                      
                        {(personData?.death_year || personData?.birth_year) && <div className='movie-metas'>
                          <div className='birth-year death-year'>
                            <h3>{personData.birth_year} - {personData.death_year}</h3>
                          </div>
                        </div>}


                    </div>
                    
                    {personData.titles_participated && 
                      <div className='movie-row'  style={{marginTop:35}}>
                          <h1 className='title-with-line'>Known For</h1>
                        
                          <div className='movies-container'>
                          {personData.titles_participated.map(title => {
                            return <MovieCard 
                                      movieID={title.title_id}
                                      imageUrl={title.image_url}
                                      movieTitle={title.title_name}
                                      averageRating={title.averageRating}
                                  />
                          })}  
                        </div>
                  


                      </div>

                  }

            </div>
            <img src={personData.image_url} className='movie-poster' />

        </div>


    </div>
  )
}
