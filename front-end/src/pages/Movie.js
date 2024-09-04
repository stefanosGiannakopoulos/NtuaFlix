import React, { useEffect, useState, useContext} from 'react'
import StarBorderIcon from '@mui/icons-material/StarBorder';
import './Movie.css'
import axiosInstance from '../api/api';
import Preloader from '../components/Preloader';
import { Link, useParams } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import { Select, MenuItem } from '@mui/material';
import { Navigate } from 'react-router-dom';



export default function Movie() {
    const { pathname } = useLocation();

    const {movieID} = useParams();
    const { user } = useContext(AuthContext);
    const { authTokens } = useContext(AuthContext);

    const [movieData, setMovieData] = useState(null);
    const [loading, setLoading] = useState(true);
    const[watchlistsStats, setWatchlistsStats] = useState(null);
    const [show_watchlists, setShowWatchlists] = useState(false);
    const [watchlists, setWatchlists] = useState([]);

    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);


    async function fetchUserWatchlists() {
        if (user){
            const response = await axiosInstance.get(`/watchlists/${user.user_id}`, {
                headers: {
                  'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`
                },
              });   
              setWatchlists(response?.data);
        }
        else{
            console.log('Not Authenticated');
            setWatchlists(null);
        }
    }

    async function fetchMovieData() {
        const response = await axiosInstance.get(`/title/${movieID}`);
        
        setMovieData(response?.data);
        setLoading(false);
    }

    async function fetchWatchlistsStats() {
        const response = await axiosInstance.get(`/number_watchlists_title/${movieID}`);
        
        setWatchlistsStats(response?.data);
    }

    useEffect(() => {
        fetchMovieData();
        fetchWatchlistsStats();
        fetchUserWatchlists();
    }, [])

    useEffect(() => {
        window.scrollTo(0, 0);
      }, [pathname]);

    function handle_watchlists () {
        if (user){
            setShowWatchlists(true);
        }
        else{
           setError("You must have a NTUAFLIX account in order to have a watchlist!")
        }
    }

    const addMovieToWatchlist = async (watchlist) => {
        setError(null);
        setSuccess(null);
            try {
                const response = await axiosInstance.post(`/watchlists/${user.user_id}/${watchlist.library_name}/add?movie_tconst=${movieID}`, null,{
                    headers: {
                    'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`
                    },
                }); 
                if (response.status == 200){
                    // console.log("Movie added successfully");
                    setSuccess("Movie added successfully!")
                }
            } catch (error) {
                setError(error?.response?.data?.detail?.msg)
                // console.log(error?.response?.data?.detail);
            }
            setShowWatchlists(false);
};

function cancelBtn() {
    setShowWatchlists(false);
    setSuccess(null);
    setError(null);
}



  if (loading) return <Preloader/>
  return (
    <div className='movie-page-container' style={{background: `linear-gradient(to right, rgba(0, 0, 0, 0.52), rgba(0, 0, 0, 0.52)), url(${movieData.titlePoster})`}}>
        <div className='movie-container mt-12'>
            
            <div className='movie-column'>
                <div className='movie-row'>
                    
                    <p className='movie-genres'>{movieData.genres.map(obj => obj.genreName).join(', ')}</p>

                    <h1 className='title-with-line'>{movieData.original_title}</h1>

                    <div className='movie-metas'>
                        {movieData.rating.avRating && <div className='movie-stars'><StarBorderIcon/><h4>{movieData.rating.avRating}/10</h4></div>}
                        {movieData.startYear && <div className='movie-year'><h4>{movieData.startYear}</h4></div>}
                        {movieData.type && <div className='movie-type'><h4>{movieData.type}</h4></div>}
                        {/* <div className='movie-duration'><h4>2h 35m</h4></div> */}
                    </div>

                    {/* <div className='movie-description'>
                        <p>When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.</p>
                    </div> */}
                    
                    <div style={{marginTop: 15, marginBottom: 15}}>
                        {watchlistsStats && Boolean(watchlistsStats.num_of_watchlists) && Boolean(watchlistsStats.num_of_users)
                            ? <p>Added by {watchlistsStats.num_of_users} users to&nbsp;
                                {watchlistsStats.num_of_watchlists} different watchlists!</p>
                            : <p>Be the first to add the title to your watchlist!</p>}
                    </div>

                    <div className='movie-actions'>
                { show_watchlists ? (
                        <div className='watchlist-dropdown'>
                            <div className='dropdown-content'>
                                                          
                            {watchlists && watchlists.map(watchlist => {
                                return <MenuItem value={watchlist.id} >
                                    <div onClick={() => addMovieToWatchlist(watchlist)} className='select-watchlist-btn'>{watchlist.library_name}</div>
                                   </MenuItem>
                            })}
                            {!watchlists && 
                            <h3>You don't have any watchlists created yet!</h3>
                            }

                            </div>
                            <button className='cancel-btn' onClick={cancelBtn}>Cancel</button>

                        </div>
                        ): (
                            <div>
                            <button className='btn btn-primary' onClick ={handle_watchlists}>Add to WatchList</button>
                            <br></br>
                            <br></br>
                            <Link to={`/makereview?revtitle=${encodeURIComponent(movieData.original_title)}`}>
                            <button className='btn btn-primary'>Make a Review</button>
                            </Link>
                            </div>
                        )}
                            {error && <p className='form-error'>{error}</p>}
                            {success && <p className='form-success'>{success}</p>}
                    </div>
        
                </div>

                {/* <div className='movie-metas'>
                    <div className='movie-stars'><StarBorderIcon/><h3>8.6/10</h3>  2.8m</div>
                    <div className='movie-year'><h3>2003</h3></div>
                    <div className='movie-duration'><h3>2h 35m</h3></div>

                </div> */}
            </div>
            <img src={movieData.titlePoster} className='movie-poster' />

        </div>

        
        <div className='movie-container mt-12'>
            <div className='movie-column'>
                        <div className='movie-row'>
                            

                            <h1 className='title-with-line'>Principals</h1>
                            {movieData.principals && 
                            <ul style={{marginTop:35}} className='principals-list'>
                                    {movieData.principals.map(principal=>{
                                        return <li> 
                                            <div>
                                            <p><Link className='a-transition' to= {`/person/${principal.nameID}`}>{principal.primaryName}</Link></p>
                                            <p>{principal.category}</p>

                                            </div> 
                                            </li>  
                                    })}
            
                            </ul>
                            }
                            
                    </div>

            </div>
        
        </div>
    </div>
  )
}
