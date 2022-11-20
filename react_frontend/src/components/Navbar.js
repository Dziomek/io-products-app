import React, {useEffect, useState} from "react";
import './Navbar.css'

function Navbar() {

    return (
        <div className='navbar-container'>
            <div className='title-container'>
                <a href="">
                  <h1>PRODUCTS APP</h1>
                </a>
            </div>
            <div className='search-container'>
                <form action="" className='search-bar'>
                    <input type="text" placeholder="Search for products..."/>
                    <button type="submit">
                        <img src={require('../images/search-icon.png')} alt=""/>
                    </button>
                </form>
            </div>
            <div className='user-container'>
                <div className='icons-container'>
                    <img src={require('../images/shopping-cart-icon.png')} alt=""/>
                    <img src={require('../images/favorite-products-icon.png')} alt=""/>
                </div>
                <div className='button-container'>
                    <a href="">
                      <button type="submit">Log in</button>
                    </a>
                </div>
            </div>
        </div>
    )
}

export default Navbar