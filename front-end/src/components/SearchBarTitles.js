import React, {useState, useEffect} from 'react'
import axiosInstance from '../api/api'
import { Autocomplete, TextField } from '@mui/material'
import { Link } from 'react-router-dom';
import './SearchBarTitles.css'
import AuthContext from '../context/AuthContext'
import { useContext } from 'react'

export default function SearchBarTitles({value, handleChangeValue}) {
    const {authTokens} = useContext(AuthContext);

    const [options, setOptions] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [loading, setLoading] = useState(false);

    async function fetchTitles() {
        const response = await axiosInstance.get(`/search-titles-autocomplete?search_title=${inputValue}` , {headers: {
            'X-OBSERVATORY-AUTH': `${authTokens ? authTokens : 'None'}`
        }});
        setLoading(false);
        setOptions(response?.data);
    }



    useEffect(() => {
        if (!inputValue) return;
        fetchTitles();
    }, [inputValue])

    return (
        <Autocomplete
        freeSolo
        sx={{width: 270}}
        value={value}
        inputValue={inputValue}
        onInputChange={(event, value) => {setInputValue(value)}}
        onChange={(event, value) => handleChangeValue(value)}
        getOptionLabel={(option) => option?.original_title ?? option}
        isOptionEqualToValue={(title, value) => title?.original_title === value?.original_title}
        loading={loading}
        loadingText={"Searching for titles..."}
        options={options}
        filterOptions={(x) => x}
        renderOption={(props, option) => (
            <li {...props} className='searchbar-option'>
                <Link to={`/movie/${option.titleID}`} className='a-transition non-underlined'>{option.original_title}</Link>
                <img className='searchbar-img' src={option.titlePoster}/>
            </li>
          )}
        renderInput={(params) => <TextField {...params} label="Search..." size='small' />}
        />
)

}
