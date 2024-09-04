import React from 'react'
import PyrforosImage from '../assets/images/pyrforos.svg'
import './Hero.css'

export default function Hero() {


    function handleScroll() {
        window.scrollTo({
            top:  window.innerHeight + 65,
            behavior: 'smooth',
          });
    }

  return (
    <section class="hero hero-gradient">
        <div class="container">

            <div class="hero-content">

                <p class="hero-subtitle">Ntua<mark>Flix</mark></p>

                <h1 class="h1 hero-title">
                    Unlimited <strong>Movies</strong>, <br/> TVs Shows, & More.
                </h1>

                <button class="btn btn-primary hero-btn" onClick={handleScroll}>
                    <span>EXPLORE</span>
                </button>

            </div>
        </div>
        <img src={PyrforosImage} className='pyrforos-image'/>  

    </section>
  )
}
