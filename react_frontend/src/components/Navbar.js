import React, {useContext, useEffect, useState} from "react";
import '../css//Navbar.css'
import {Link} from "react-router-dom";
import {Context} from "../store/appContext";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCartShopping, faStar} from '@fortawesome/free-solid-svg-icons'

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
                        <FontAwesomeIcon icon={faStar} className="navbar-icon"/>
                    </Link>
                    <Link to='/'>
                        <FontAwesomeIcon icon={faCartShopping} className="navbar-icon"/>
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