import React, {useContext, useState, useEffect, useRef} from 'react'
import { Context } from '../store/appContext'
import '../css/LoginAndRegisterForm.css'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faKey, faEnvelope, faK} from '@fortawesome/free-solid-svg-icons'

const LoginForm = () => {

    const {store, actions} = useContext(Context)
    const [errorMessage, setErrorMessage] = useState(null)
    
    const emailInput = useRef()
    const passwordInput = useRef()

    const login = () => {
        const options = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: emailInput.current.value,
                password: passwordInput.current.value
            })
        }
        console.log(emailInput.current.value, passwordInput.current.value)
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
                    
                }
            })
            .catch(error => {
                setErrorMessage("Invalid credentials. Please try again")
            })
    }

    return (
        <div className='login-modal-form'>
            <div className='form-inner-container'>
                <FontAwesomeIcon icon={faEnvelope} className='login-form-icon'/>
                <input type='text' placeholder='email...' ref={emailInput}></input>
            </div>
            <div className='form-inner-container'>
                <FontAwesomeIcon icon={faKey} className='login-form-icon'/>
                <input type='password' placeholder='password...' ref={passwordInput}></input>
            </div>
            <div className='form-inner-container'>
                <p style={{margin: '0', color: 'red'}}>{errorMessage}</p>
            </div>
            <div className='login-form-footer'>
                <button type='button' onClick={login}>SIGN IN</button>
            </div>
        </div>
    )
}

export default LoginForm