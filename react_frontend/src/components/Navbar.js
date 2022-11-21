import React, {useContext, useEffect, useState} from "react";
import './Navbar.css'
import {Link} from "react-router-dom";
import {Context} from "../store/appContext";

function Navbar() {

    const {store, actions} = useContext(Context)

    return (
        <div className='navbar-container'>
            <div className='title-container'>
                <Link to="/">
                  <h1>PRODUCTS APP</h1>
                </Link>
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
                    { !store.token ?
                        <Link to="/login">
                            <button type="submit">Login</button>
                        </Link>
                        :
                        <button onClick={() => actions.logout()}>Logout</button>
                    }
                </div>
            </div>
        </div>
    )
}

export default Navbar