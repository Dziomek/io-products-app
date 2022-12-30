import React from "react";
import {Link, useNavigate} from "react-router-dom";
import {useContext, useEffect, useState, useRef} from "react";
import {Context} from "../store/appContext";
import './Register.css'
import {faEnvelope, faKey, faPlus, faCheck, faUser, faHouse} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";



function Register() {
    const navigate = useNavigate()
    const {store, actions} = useContext(Context)
    const [errorMessage, setErrorMessage] = useState(null)

    const usernameInput = useRef()
    const emailInput = useRef()
    const passwordInput = useRef()
    const confirmPasswordInput = useRef()

    const submitRegistration = () => {
        const username = usernameInput.current.value
        const email = emailInput.current.value
        const password = passwordInput.current.value
        const confirmPassword = confirmPasswordInput.current.value

        const options = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
                confirmPassword: confirmPassword
            })
        }
        fetch("http://127.0.0.1:5000/register_user", options)
            .then(response => {
                if(response.status === 200) return response.json()
            })
            .then(data => {
                console.log(data)
                if(data.message === "User succesfully created") {
                    sessionStorage.setItem("emailToConfirm", data.email)
                    actions.register(data.email)
                    navigate('/confirm')
                }
                else setErrorMessage(data.message)
            })
            .catch(error => {
                console.error("An error occured")
                setErrorMessage('siemanko')
            })
    }

    useEffect(() => {
        console.log('TOKEN', store.token)
        if(store.token) navigate('/')
    }, [store.token])

    useEffect(() => {
        actions.syncDataFromSessionStorage()
    }, [])

    return(
        <>
            <div className='login-container'>
                <div className="login-title">
                    <h2>Create new</h2>
                    <h1>ACCOUNT</h1>
                </div>
                <div className="login-form">
                    <div className="inner-container no-margin">
                        <FontAwesomeIcon icon={faPlus} className="register-icon"/>
                    </div>
                    <div className="error-container">
                        <p>{errorMessage}</p>
                    </div>
                    <div className="inner-container input no-margin">
                        <FontAwesomeIcon icon={faUser} className="login-icon"/>
                        <input type="username" name="username" placeholder="username" ref={usernameInput}/>
                    </div>
                    <div className="inner-container input">
                        <FontAwesomeIcon icon={faEnvelope} className="login-icon"/>
                        <input type="text" name="email" placeholder="email" ref={emailInput}/>
                    </div>
                    <div className="inner-container input">
                        <FontAwesomeIcon icon={faKey} className="login-icon"/>
                        <input type="password" name="password" placeholder="password" ref={passwordInput}/>
                    </div>
                    <div className="inner-container input">
                        <FontAwesomeIcon icon={faCheck} className="login-icon"/>
                        <input type="password" name="confirm-password" placeholder="confirm password" ref={confirmPasswordInput}/>
                    </div>
                    <div className="spacer"></div>
                    <div className="inner-container">
                        <button type="submit" onClick={submitRegistration}>Register</button>
                    </div>
                    <div className="inner-container less-margin">
                        <Link to='/'>
                            <button>
                                <FontAwesomeIcon icon={faHouse} className="button-icon"/>
                                Back to home page
                            </button>
                        </Link>
                    </div>
                </div>
            </div>
        </>
    )
}
export default Register