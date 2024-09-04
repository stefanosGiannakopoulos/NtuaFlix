import {Navigate} from 'react-router-dom';
import  AuthContext  from '../context/AuthContext';
import {useContext} from "react";
import { useNavigate } from "react-router-dom";

const UserProtectedRoute = ({children}) => {
    const navigate = useNavigate();
    const {user} = useContext(AuthContext);
    
    if (!user) return <Navigate to='/auth/login/' />
    return children;
}

export default UserProtectedRoute;
