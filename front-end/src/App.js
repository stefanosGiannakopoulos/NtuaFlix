import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import Index from './pages/Index';
import Auth from './pages/auth/Auth';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import Navbar from './components/Navbar';
import Movie from './pages/Movie';
import Movies from './pages/Movies';
import { AuthProvider } from './context/AuthContext';
import Watchlist from './pages/Watchlist';
import Recommender from './pages/Recommender';
import Person from './pages/Person';
import ForgotPassword from './pages/auth/ForgotPassword';
import ResetPassword from './pages/auth/ResetPassword';
import LibContents from './pages/LibContents';
import Reviews from './pages/Reviews';
import NewReview from './pages/MakeReview';
import Profile from './pages/Profile';
import Statistics from './pages/Statistics';
import CopyrightNotice from './components/CopyrightNotice';
import WatchlistStats from './pages/WatchlistStats';
import ReviewsStats from './pages/ReviewsStats';

import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import UserProtectedRoute from './utils/UserProtectedRoute';


const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});


function App() {
  
  return (
    <ThemeProvider theme={darkTheme}><CssBaseline />
      <div className="App">
        <Router>
          <AuthProvider>
            <Navbar/>

            <Routes>
              <Route path='/' exact element={<Index />} />
              <Route path='/movie/:movieID/' exact element={<Movie />} />
              <Route path='/person/:personID/' exact element={<Person />} />
              <Route path='/movies/' exact element={<Movies />} />

              <Route path='/recommend/' exact element={<Recommender />} />

              <Route path='/watchlist/'  element={<Watchlist />} />
              <Route path='/reviews/' exact element = {<UserProtectedRoute><Reviews /></UserProtectedRoute>} />
              <Route path='/makereview/:revtitle?' exact element = {<UserProtectedRoute><NewReview /></UserProtectedRoute>} />
              <Route path='/libcontents/:library_name/' exact element={<UserProtectedRoute><LibContents /></UserProtectedRoute>} />
              <Route path='/account/profile' element={<UserProtectedRoute><Profile/></UserProtectedRoute>} />
              <Route path='/account/statistics/' exact element = {<UserProtectedRoute><Statistics /></UserProtectedRoute>} />
              <Route path='/account/statistics/watchlists/' exact element = {<UserProtectedRoute><WatchlistStats /></UserProtectedRoute>} />
              <Route path='/account/statistics/reviews/' exact element = {<UserProtectedRoute><ReviewsStats /></UserProtectedRoute>} />


              <Route path='/auth' exact element={<Auth/>}>
                <Route path='login/' element={<Login/>} />
                <Route path='register/' element={<Register/>} />
                <Route path='forgot-password/' element={<ForgotPassword />} />
                <Route path='reset-password/:secretToken/' element={<ResetPassword />} />
              </Route>


            </Routes>
          </AuthProvider>
          <CopyrightNotice />
        </Router>
      </div>
    </ThemeProvider>

  );
}

export default App;
