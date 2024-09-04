import React from 'react'
import './LibContent.css'
import { Link } from 'react-router-dom'
import { CgYoutube , CgPlayListRemove } from "react-icons/cg";

const LibContent = ({ movies }) => {
    return (
      <div className="watchlist-container">
        <table className="watchlist-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Movie Title</th>
            </tr>
          </thead>
          <tbody>
            {movies.map((movie, index) => (
              <tr key={index} className={index % 2 === 0 ? 'even-row' : 'odd-row'}>
                <td>{index + 1}</td>
                <td>{movie.originalTitle} {movie.image_url}</td>
                <td><Link to='/movie'><CgYoutube /></Link></td>
                <td>
                <button className="delete-button"><CgPlayListRemove/></button>
              </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };
  
  export default LibContent;