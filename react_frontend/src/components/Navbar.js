import React, {useContext, useEffect, useState} from "react";
import './Navbar.css'
import {Link} from "react-router-dom";
import {Context} from "../store/appContext";

function Navbar() {

    const {store, actions} = useContext(Context)

    return (
        <div className='navbar-container'>
            <section className='title-container'>
                <Link to="/">
                  <h1>PRODUCTS APP</h1>
                </Link>
            </section>
            <section className='search-container'>
                <form action="" className='search-bar'>
                    <input type="text" placeholder="Search for products..."/>
                    <button type="submit">
                        <img src={require('../images/search-icon.png')} alt=""/>
                    </button>
                </form>
            </section>
            <section className='user-container'>
                <div className='icons-container'>
                    <Link to='/'>
                        <img src={require('../images/shopping-cart-icon.png')} alt=""/>
                    </Link>
                    <Link to='/'>
                        <img src={require('../images/favorite-products-icon.png')} alt=""/>
                    </Link>
                </div>
                <div className='button-container'>
                    { !store.token ?
                        <div>
                            <Link to="/login">
                               <button type="submit">Log in</button>
                            </Link>
                            <Link to="/register">
                                <button type="submit">Register</button>
                            </Link>
                        </div>
                        :
                        <div>
                            <h1>{store.username}</h1>
                            <button onClick={() => actions.logout()}>Log out</button>
                        </div>
                    }
                </div>
            </section>
        </div>
    )
}

export default Navbar