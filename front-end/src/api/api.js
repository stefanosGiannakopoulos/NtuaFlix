import axios from "axios";




const axiosInstance = axios.create({
    // this is the base url
    baseURL: 'http://127.0.0.1:9876/ntuaflix_api/',
    headers: {
        'Content-Type': 'application/json',        
    }
})


export default axiosInstance;
