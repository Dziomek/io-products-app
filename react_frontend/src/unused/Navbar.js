import React, {useContext, useEffect, useState} from "react";
import '../css//Navbar.css'
import {Link} from "react-router-dom";
import {Context} from "../store/appContext";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCartShopping, faStar} from '@fortawesome/free-solid-svg-icons'
import LoginRegisterModal from "./LoginRegisterModal";

function Navbar() {

    const {store, actions} = useContext(Context)

    return (
        <div className='navbar-container'>
            <section className='title-container'>
                <Link to="/">
                  <h1 >PRODUCTS <p className="title2">APP</p></h1>
                </Link>
            </section>
            <div className='button-container'>
                    { !store.token ?
                        <div>
                            <LoginRegisterModal/>
                        </div>
                        :
                        <div>
                            <h1>{store.username}</h1>
                            <button onClick={() => actions.logout()}>Log out</button>
                        </div>
                    }
                </div>
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
            </section>
        </div>
    )
}

export default Navbar