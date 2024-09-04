import React from 'react'
import AuthContext from '../context/AuthContext'
import { useContext, useEffect, useState, useMemo } from 'react'
import NotRegistered from './NotRegistered';
import axiosInstance from '../api/api'
import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom'
import { CgPlayListAdd, CgTrash, CgYoutube , CgPlayListRemove, CgSearch} from "react-icons/cg";
import './LibContents.css' 
import NoImageFound from '../assets/images/NoImagePrev.png'

export default function LibContents() {

    const {user} = useContext(AuthContext);
    const { authTokens } = useContext(AuthContext);
    const { library_name } = useParams();

    const response_dict = useMemo(() => ({
      204: `${library_name}: This watchlist is empty!`,
      403: `${library_name}: This watchlist doesn't belong to you!`,
      404: `${library_name}: This Watchlist doesn't exist!`,
      401: 'You must sign in first! ',
    }), [library_name]);

    const [movies, setMovies] = useState([]); 
    const [status, setStatus]= useState(null);
    const [adding, setAdding] = useState(false);
    const [title, setTitle] = useState('');
    const [addingMovie, setAddingMovie] = useState(null);

    
    useEffect(() => {
        const fetchLibContents = async () => {
          try {
            const response = await axiosInstance.get(`/watchlists/${user.user_id}/${library_name}`, {
              headers: {
                'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`
              },
            });
    
            if (response.status === 200) {
              setMovies(response?.data);
            }
            else {
                setStatus(response.status);
            }
          } catch (error) {
            if (error.response && error.response.status in response_dict) {
                setStatus(error.response.status);
            }
            console.error(`Error fetching contents for ${library_name}:`, error);
          }
          console.log(movies);
        };
    
        fetchLibContents();
      }, [user?.user_id, authTokens,library_name]);
      

      const removeWatchlist = async () => {
        try {
          const response = await axiosInstance.delete(`/watchlists/${user.user_id}/${library_name}`, {
            headers: {
              'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`,
            },
          });
          if (response.status === 200) {
            console.log("Lib deleted successfully");
            window.location.reload();
          }
        }
          catch (error){
            console.error(error.status);
          }
          
        };

        const removeMovie = async (movie) => {
          try{
            const response = await axiosInstance.delete(`/watchlists/${user.user_id}/${library_name}/remove?movie_tconst=${movie.titleID}`, {
              headers: {
                'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`,
              },
            });
            if (response.status === 200){
              console.log("Movie remoced successfully");
              window.location.reload();
            }
          }catch (error){
            console.log(error.status);
          }
        };

        const fetchMovie = async (e) =>{
          e.preventDefault();
          try {
          const response = await axiosInstance.get(`/search-titles-autocomplete?search_title=${title}`, {
            headers: {
              'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`
              },
          
          });
          if (response.status===200){
            setAddingMovie(response?.data);
            console.log(addingMovie, title, response);
          }
        }catch(error){
          console.log(error.status);
        }
        setTitle('');
        }
      
      const add_movie = async (movie_id) => {
        try {
          const response = axiosInstance.post(`/watchlists/${user.user_id}/${library_name}/add?movie_tconst=${movie_id}`, null,{
              headers: {
              'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`
              },
          }); 
          console.log(response.status);
          if (response.status==200){
              console.log("Movie added successfully");
              window.location.reload();
          }
          } catch (error){
              console.log(error.status);
          } finally {
          setAdding(false);
          setAddingMovie([]);
          setTitle(''); 
          window.location.reload();
          }
      }

    if (!user) return <NotRegistered />

    return (
        <>

          {status && status !==204? (
            <div>
                <h2 className="watchlist-title">{response_dict[status]}</h2>
             
            </div>
          ) :

          (
            <div>
              {status ===204 &&
              <h2 className="watchlist-title">{response_dict[status]}</h2>
              }
              {!status && 
              <div>
            <h1 className="watchlist-title">All movies in '{library_name}'</h1>
              
           

         
            <div className="watchlist-container">
          <table className="watchlist-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Movie Title</th>
            </tr>
          </thead>
          <tbody>
            {movies && movies.map((movie, index) => (
              <tr key={index} className={index % 2 === 0 ? 'even-row' : 'odd-row'}>
                <td>{index + 1}</td>
                <td><Link to={`/movie/${movie.titleID}`} className='movie-table'>{movie.original_title}</Link></td>
                <td><img src={movie.titlePoster ? movie.titlePoster : NoImageFound}
                 alt="Movie Poster" className="poster-prev"/></td>
                <td>
                <button className="delete-button" onClick={()=>removeMovie(movie)}><CgPlayListRemove/></button>
              </td>
              </tr>
            ))}
            </tbody>
          </table>
          </div>
          </div>
          }

          {/* <div className='watchlist-button-container'>
            <button className='btn btn-primary add-movie button-align-center' onClick ={()=>setAdding(true)}> 
              <CgPlayListAdd />Add Movies 
              </button>
              <button className='btn btn-primary remove-lib button-align-center' 
            onClick={removeWatchlist}><CgTrash/>Delete {library_name}
            </button>
         </div> */}
          <div className='watchlist-button-container'>
              <button className='btn btn-primary add-movie button-align-center' onClick ={()=>setAdding(true)}> 
                <CgPlayListAdd />Add Movies
              </button>
              {adding && (
         <div className='vertical-form-container'>
          <form className='vertical-form' onSubmit={fetchMovie}>
            <div>
            <input value={title} onChange = {(e) => setTitle(e.target.value)} 
             type="text" placeholder="Enter Original Title" id="title" name="title" required/>
             <button><CgSearch/></button>
             </div>
          </form>
          </div>
          
    

        )} 
              <button className='btn btn-primary remove-lib button-align-center' onClick={removeWatchlist}>
                  <CgTrash/>Delete {library_name}
              </button>
          </div>

             

            {addingMovie && (
          
          addingMovie.map((movie) => (
            <div key={movie.titleID} className="image-container">
            <img src={movie.titlePoster ? movie.titlePoster : NoImageFound} alt="Fetched Image" />
            <span>{movie.original_title}</span>
            <button className='add-movie-btn' onClick={() => add_movie(movie.titleID)}>Add</button>
          </div>
          )
          
        ))} 


         
            </div>
            
          )}

          </>
      );
      
}