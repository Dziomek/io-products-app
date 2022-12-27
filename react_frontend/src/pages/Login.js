import '../css/Login.css'
import {useEffect, useState, useContext} from "react";
import {Link, useNavigate} from 'react-router-dom'
import {Context} from "../store/appContext";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faKey, faEnvelope} from '@fortawesome/free-solid-svg-icons'
import {faUser} from '@fortawesome/free-regular-svg-icons'
import React from "react";

function Login() {
    const navigate = useNavigate()
    const {store, actions} = useContext(Context)
    const [errorMessage, setErrorMessage] = useState(null)
    const [email, setEmail] = useState(null)
    const [password, setPassword] = useState(null)

    const handleClick = () => {
        const options = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        }
        fetch("http://127.0.0.1:5000/token", options)
            .then(response => {
                console.log('Response status:', response.status)
                if (response.status !== 200) {
                    setErrorMessage("Invalid credentials. Please try again")
                }
                return response.json()
            })
            .then(data => {
                console.log(data)
                sessionStorage.setItem("is_active", data.is_active)
                sessionStorage.setItem("emailToConfirm", data.email)
                if(data.is_active) {
                    sessionStorage.setItem("username", data.username)
                    sessionStorage.setItem("email", data.email)
                    sessionStorage.setItem("token", data.access_token)
                    if (sessionStorage.getItem("emailToConfirm")) sessionStorage.removeItem("emailToConfirm")
                    actions.login(data.access_token, data.username, data.email, data.is_active)
                    navigate('/')
                }
                else {
                    navigate('/confirm')
                }
            })
            .catch(error => {
                setErrorMessage("Invalid credentials. Please try again")
            })
    }

    useEffect(() => {
        if(store.token) navigate('/')
    }, [store.token])

    useEffect(() => {
        actions.syncDataFromSessionStorage()
    }, [])

    return(
        <>
            <div className='login-container'>
                <div className="login-title">
                    <h2>Log in to</h2>
                    <h1>PRODUCTS APP</h1>
                </div>
                <div className="login-form" >
                    <div className="form-icon">
                        <img src={require('../images/user-icon.png')} alt=""/>
                    </div>
                    <div className="error-container">
                        <p>{errorMessage}</p>
                    </div>
                    <div className="inner-container input">
                        <FontAwesomeIcon icon={faEnvelope} className="login-icon"/>
                        <input type="text" name="email" placeholder="email" onChange={
                            (e) => setEmail(e.target.value)}/>
                    </div>
                    <div className="inner-container input">
                        <FontAwesomeIcon icon={faKey} className="login-icon"/>
                        <input type="password" name="password" placeholder="password" onChange={
                                (e) => setPassword(e.target.value)}/>
                    </div>
                    <div className="spacer"></div>
                    <div className="inner-container">
                        <button type="submit" onClick={handleClick}>Log in</button>
                    </div>
                    <div className="inner-container less-margin">
                        <Link to='/'>
                            <button>
                                <FontAwesomeIcon icon={faUser} className="button-icon"/>
                                Continue as a guest
                            </button>
                        </Link>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Login