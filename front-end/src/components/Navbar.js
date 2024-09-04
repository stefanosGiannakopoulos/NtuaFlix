import React, {useEffect} from 'react'
import './Navbar.css'
import { NavLink } from 'react-router-dom'
import { matchPath, } from 'react-router-dom'
import {useLocation} from 'react-router-dom'
import MenuIcon from '@mui/icons-material/Menu';
import AuthContext from '../context/AuthContext'
import { useContext } from 'react'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

export default function Navbar() {

const {logoutUser, user} = useContext(AuthContext);

  const location = useLocation();
  const match = matchPath({path:`/`, exact:true}, location.pathname)



  useEffect( () => {
    var duplicateScript = document.getElementById("navbarScript");
    if (duplicateScript) return;
    const inlineScript = document.createElement('script');
    inlineScript.setAttribute("id", "navbarScript");
    inlineScript.innerHTML = `
    const toggle = document.querySelector(".toggle");
    const menu = document.querySelector(".menu");
    const items = document.querySelectorAll(".item");
    const logo = document.querySelector("nav ul.menu .logo")
    const nav = document.getElementById("#top-nav");


    /* Toggle mobile menu */
    function toggleMenu() {
      if (window.innerWidth < 1078) { /* This item is new. Only if the user is using a mobile phone toggle the active class */
      if (menu.classList.contains("active")) {
        menu.classList.remove("active");
        //toggle.querySelector("a").innerHTML = "<i class='fas fa-bars'></i>";
        toggle.querySelector("a").innerHTML = "<svg class='MuiSvgIcon-root MuiSvgIcon-fontSizeMedium css-i4bv87-MuiSvgIcon-root css-vubbuv' focusable='false' aria-hidden='true' viewBox='0 0 24 24' data-testid='MenuIcon'><path d='M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z'></path></svg>"
      } else {
        menu.classList.add("active");
        //toggle.querySelector("a").innerHTML = "<i class='fas fa-times'></i>";
        toggle.querySelector("a").innerHTML = "<svg class='MuiSvgIcon-root MuiSvgIcon-fontSizeMedium css-i4bv87-MuiSvgIcon-root css-vubbuv' focusable='false' aria-hidden='true' viewBox='0 0 24 24' data-testid='CloseIcon'><path d='M19 6.41 17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z'></path></svg>"
      }
    } 

    }
    
  
    
    /* Activate Submenu */
    function toggleItem() {
      if (this.classList.contains("submenu-active")) {
        this.classList.remove("submenu-active");
      } else if (menu.querySelector(".submenu-active")) {
        menu.querySelector(".submenu-active").classList.remove("submenu-active");
        this.classList.add("submenu-active");
      } else {
        this.classList.add("submenu-active");
      }
    }
    
    /* Close Submenu From Anywhere */
    function closeSubmenu(e) {
      if (menu.querySelector(".submenu-active")) {
        let isClickInside = menu
          .querySelector(".submenu-active")
          .contains(e.target);
    
        if (!isClickInside && menu.querySelector(".submenu-active")) {
          menu.querySelector(".submenu-active").classList.remove("submenu-active");
        }
      }
    }
   


    /* when clicking on the logo, the menu must be closed no matter what! NOT TOGGLED (if the menu is not active by pressing on the logo it will open)*/
    function closeMenu() {
    if (window.innerWidth < 1078) { /* This item is new. Only if the user is using a mobile phone toggle the active class */
    if (menu.classList.contains("active")) {
      menu.classList.remove("active");
      //toggle.querySelector("a").innerHTML = "<i class='fas fa-bars'></i>";
      toggle.querySelector("a").innerHTML = "<svg class='MuiSvgIcon-root MuiSvgIcon-fontSizeMedium css-i4bv87-MuiSvgIcon-root css-vubbuv' focusable='false' aria-hidden='true' viewBox='0 0 24 24' data-testid='MenuIcon'><path d='M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z'></path></svg>"

    }
  } 
    }

    /* Event Listeners */
    toggle.addEventListener("click", toggleMenu, false);
    logo.addEventListener("click", closeMenu, false); /* this is new. If logo is clicked, toggle navbar */

    for (let item of items) {
        if (!item.querySelector(".submenu")) { /* this if statement is new. If item is not a dropdown then if it is clicked, automatically toggle navbar */
          item.addEventListener("click", toggleMenu, false);
        }

        if (item.querySelector(".submenu")) {
        item.addEventListener("click", toggleItem, false);
        }
        item.addEventListener("keypress", toggleItem, false);
    }
    document.querySelectorAll(".subitem").forEach((item) => item.addEventListener("click", toggleMenu, false)) /* this if statement is new. If item is in a dropdown then if it is clicked, automatically toggle navbar */
    document.addEventListener("click", closeSubmenu, false);
    `
    document.body.append(inlineScript);
  }, [])


  return (
    <>

    {/* <nav className={`navigation ${!match && 'colored'}`} id='#top-nav' role='navigation' aria-label='Main navigation'> */}
    <nav className={`navigation ${!match}`} id='top-nav' role='navigation' aria-label='Main navigation'>
        <ul className="menu">
          {/* <li className="logo"><NavLink className='not-color' to={`/`}><img src={NtuaflixLogo} width="85" alt='IEEE NTUA Student Branch.' /></NavLink></li> */}
          <li className="logo"><NavLink className='not-color' to={`/`}><h1>Ntua<mark>flix</mark></h1></NavLink></li>

          <li className="item"><NavLink to={`/`}>Home</NavLink></li>
          {/* <li className="item"><NavLink to={`/profile`}>Profile</NavLink></li> */}
          <li className="item"><NavLink to={`/movies`}>Movies</NavLink></li>
          {/* <li className="item"><NavLink to={`/watchlist/`}>WatchLists</NavLink></li>
          <li className="item"><NavLink to={`/reviews/`}>Reviews</NavLink></li> */}
          {/* <li className="item"><NavLink to={`/statistics/`}>Statistics</NavLink></li> */}
          <li className="item"><NavLink to={`/recommend/`}>Recommender</NavLink></li>
          <li className='item'><NavLink to={`/watchlist`}>Watchlist</NavLink></li>
          
          <li className={`item has-submenu ${!user && 'hidden'}`}>
            <a tabIndex="0">Account Info<ExpandMoreIcon/></a>
            <ul className="submenu">
              <li className="subitem"><NavLink to={`/account/profile`} className='subitem-link'>Profile</NavLink></li>
              <li className="subitem"><NavLink to={`/account/statistics`} className='subitem-link'>Statistics</NavLink></li>
              <li className="subitem"><NavLink to={`/watchlist`} className='subitem-link'>WatchLists</NavLink></li>
              <li className="subitem"><NavLink to={`/reviews`} className='subitem-link'>Reviews</NavLink></li>
            </ul>
          </li>

          
          {/* <li class="item has-submenu">
            <a tabIndex="0">Projects</a>
            <ul class="submenu">
              <li class="subitem"><a href="#">Freelancer</a></li>
              <li class="subitem"><a href="#">Startup</a></li>
              <li class="subitem"><a href="#">Enterprise</a></li>
            </ul>
          </li> */}

           {!user &&  <li className="item">
              <NavLink to={`/auth/register`} className='not-color cta' >
                <span> Sign up/in </span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -13.54 122.88 122.88"><path d="M12.14 0h98.6c3.34 0 6.38 1.37 8.58 3.56 2.2 2.2 3.56 5.24 3.56 8.58v71.47c0 3.34-1.37 6.38-3.56 8.58a12.11 12.11 0 0 1-8.58 3.56h-19.2c-.16.03-.33.04-.51.04-.17 0-.34-.01-.51-.04H62.74c-.16.03-.33.04-.51.04-.17 0-.34-.01-.51-.04H33.31c-.16.03-.33.04-.51.04-.17 0-.34-.01-.51-.04H12.14c-3.34 0-6.38-1.37-8.58-3.56S0 86.95 0 83.61V12.14C0 8.8 1.37 5.76 3.56 3.56 5.76 1.37 8.8 0 12.14 0zm43.05 31.24 20.53 14.32a2.92 2.92 0 0 1 .1 4.87L55.37 64.57a2.928 2.928 0 0 1-4.78-2.27V33.63h.01c0-.58.17-1.16.52-1.67a2.93 2.93 0 0 1 4.07-.72zm38.76 48.21V89.9h16.78c1.73 0 3.3-.71 4.44-1.85a6.267 6.267 0 0 0 1.85-4.44v-4.16H93.95zM88.1 89.9V79.45H65.16V89.9H88.1zm-28.79 0V79.45H35.73V89.9h23.58zm-29.44 0V79.45H5.85v4.16c0 1.73.71 3.3 1.85 4.44a6.267 6.267 0 0 0 4.44 1.85h17.73zM5.85 73.6h111.18V22.2H5.85v51.4zM88.1 16.35V5.85H65.16v10.49H88.1v.01zm5.85-10.5v10.49h23.07v-4.2c0-1.73-.71-3.3-1.85-4.44a6.267 6.267 0 0 0-4.44-1.85H93.95zm-34.64 10.5V5.85H35.73v10.49h23.58v.01zm-29.44 0V5.85H12.14c-1.73 0-3.3.71-4.44 1.85a6.267 6.267 0 0 0-1.85 4.44v4.2h24.02v.01z"/></svg>               

              </NavLink>
            </li>}
            {user && <li className="item"><NavLink to={'#'} className='not-color cta' onClick={logoutUser}><span>logout</span><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M14.945 1.25c-1.367 0-2.47 0-3.337.117-.9.12-1.658.38-2.26.981-.524.525-.79 1.17-.929 1.928-.135.737-.161 1.638-.167 2.72a.75.75 0 0 0 1.5.008c.006-1.093.034-1.868.142-2.457.105-.566.272-.895.515-1.138.277-.277.666-.457 1.4-.556.755-.101 1.756-.103 3.191-.103h1c1.436 0 2.437.002 3.192.103.734.099 1.122.28 1.4.556.276.277.456.665.555 1.4.102.754.103 1.756.103 3.191v8c0 1.435-.001 2.436-.103 3.192-.099.734-.279 1.122-.556 1.399-.277.277-.665.457-1.399.556-.755.101-1.756.103-3.192.103h-1c-1.435 0-2.436-.002-3.192-.103-.733-.099-1.122-.28-1.399-.556-.243-.244-.41-.572-.515-1.138-.108-.589-.136-1.364-.142-2.457a.75.75 0 1 0-1.5.008c.006 1.082.032 1.983.167 2.72.14.758.405 1.403.93 1.928.601.602 1.36.86 2.26.982.866.116 1.969.116 3.336.116h1.11c1.368 0 2.47 0 3.337-.116.9-.122 1.658-.38 2.26-.982.602-.602.86-1.36.982-2.26.116-.867.116-1.97.116-3.337v-8.11c0-1.367 0-2.47-.116-3.337-.121-.9-.38-1.658-.982-2.26-.602-.602-1.36-.86-2.26-.981-.867-.117-1.97-.117-3.337-.117h-1.11Z" fill="#fff"/><path d="M15 11.25a.75.75 0 0 1 0 1.5H4.027l1.961 1.68a.75.75 0 1 1-.976 1.14l-3.5-3a.75.75 0 0 1 0-1.14l3.5-3a.75.75 0 1 1 .976 1.14l-1.96 1.68H15Z" fill="#fff"/></svg></NavLink></li>}
        <li className="toggle"><a href="#"><MenuIcon/></a></li>

        </ul>
      </nav>
      </>
  )
}
