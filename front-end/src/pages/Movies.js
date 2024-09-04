import React, { useEffect, useState } from 'react'
import MovieCard from '../components/MovieCard'
import Preloader from '../components/Preloader'
import axiosInstance from '../api/api'
import Pagination from '@mui/material/Pagination'
import SearchBarTitles from '../components/SearchBarTitles'
import { Select, MenuItem } from '@mui/material'
import { useLocation } from 'react-router-dom';
import AuthContext from '../context/AuthContext'
import { useContext } from 'react'
import NoMovieImage from '../assets/no-movie-found.svg'
import './Movies.css'


export default function Movies() {
  const { pathname } = useLocation();

  const {authTokens} = useContext(AuthContext);

  const location = useLocation();
  const genreQuery = new URLSearchParams(location.search);
  const genreUrlParam = genreQuery.get('genre');

    const NO_GENRE_SELECTED_STRING = "none";

    const [genre, setGenre] = useState(!genreUrlParam ? NO_GENRE_SELECTED_STRING : genreUrlParam);
    const [titles, setTitles] = useState(null);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);
    const [searchValue, setSearchValue] = useState(null);
    const [genres, setGenres] = useState(null);
    const [totalPages, setTotalPages] = useState(null);



    async function fetchGenres() {
      const response = await axiosInstance.get('/get-genres');
      setGenres(response?.data);
    }

    async function fetchTitles(wait_in_func = true) {
      if (wait_in_func)
        setLoading(true)
      let genrePayload = genre === NO_GENRE_SELECTED_STRING ? "" : parseInt(genre);
      const response = await axiosInstance.get(`/get-movies?page=${page}${genrePayload ? `&qgenre=${genrePayload}` : ''}`, {headers: {
        'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`
    }});
      setTitles(response?.data?.titles);
      if (response?.data?.total_pages)
      setTotalPages(parseInt(response?.data?.total_pages))
      if (wait_in_func)
        setLoading(false)
    }

    useEffect(() => {
        if (genre === '' || genre === undefined) return;

        if (page === 1) fetchTitles(true);
        else setPage(1);
    }, [genre])

    useEffect( () => {
        const callBoth = async() => {
          setLoading(true);
          if (!genres)
              await fetchGenres();
          await fetchTitles(false);

          setLoading(false);
        }

        callBoth();

    }, [page])

    useEffect(() => {
      window.scrollTo(0, 0);
    }, [pathname]);


  if (loading) return <Preloader />


  return (
    <div className='page-container'>


      <div className='filters'>
        <div className='filters-column'>
        <SearchBarTitles value={searchValue} handleChangeValue={(value) => {setSearchValue(value)}} />
        <Select
          labelId="demo-select-small-label"
          id="demo-select-small"
          value={genre}
          label="All Genres"
          onChange={(e) => setGenre(e.target.value)}
          size='small'
          sx={{width: 170}}
          
        >
          <MenuItem value={NO_GENRE_SELECTED_STRING} selected>
            All Genres
          </MenuItem>
          {genres && genres.map(genreItem => {
            return <MenuItem value={genreItem.id}>{genreItem.name}</MenuItem>
          })}
      </Select>
        </div>
        <div className='filters-column'>
          <Pagination count={totalPages} page={page} onChange={(event,value) => {setPage(value);}}/>
        </div>
      </div>
        <div className='movies-container'>
 
            {titles && titles.map((title) => {
              return <MovieCard 
                key={title.titleID} 
                movieID={title.titleID} 
                movieTitle={title.original_title} 
                averageRating={title.rating.avRating} 
                imageUrl={title?.titlePoster}/>
            })}

            {titles.length === 0 && <div className='no-movie-found'>
                  <h3>No Movie Found :(</h3>
                  <img src={NoMovieImage} />
                  
              
              </div>}

        </div>
          
          <div className='filters'>
            <div className='filters-column flex-end'>
              <Pagination count={totalPages} page={page} onChange={(event,value) => {setPage(value);}}/>
            </div>
        </div>
    </div>
  )
}
