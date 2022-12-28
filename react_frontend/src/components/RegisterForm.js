import React, {useContext, useState, useEffect, useRef} from 'react'
import { Context } from '../store/appContext'
import '../css/LoginAndRegisterForm.css'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faKey, faEnvelope, faUser, faCheck} from '@fortawesome/free-solid-svg-icons'

const RegisterForm = () => {
    
    const {store, actions} = useContext(Context)
    const [errorMessage, setErrorMessage] = useState(null)

    const emailInput = useRef()
    const passwordInput = useRef()
    const usernameInput = useRef()
    const confirmPasswordInput = useRef()
    
    const register = () => {
        const username = usernameInput.current.value
        const email = emailInput.current.value
        const password = passwordInput.current.value
        const confirmPassword = confirmPasswordInput.current.value

        console.log(username, email, password, confirmPassword)

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
                    // navigate('/confirm')
                }
                else setErrorMessage(data.message)
            })
            .catch(error => {
                console.error("An error occured")
                setErrorMessage('siemanko')
            })
    }
    return (
        <div className='register-modal-form'>
            <div className='form-inner-container'>
                <FontAwesomeIcon icon={faUser} className='register-form-icon'/>
                <input type='text' placeholder='username...' ref={usernameInput}></input>
            </div>
            <div className='form-inner-container'>
                <FontAwesomeIcon icon={faEnvelope} className='register-form-icon'/>
                <input type='text' placeholder='email...' ref={emailInput}></input>
            </div>
            <div className='form-inner-container'>
                <FontAwesomeIcon icon={faKey} className='register-form-icon'/>
                <input type='password' placeholder='password...' ref={passwordInput}></input>
            </div>
            <div className='form-inner-container'>
                <FontAwesomeIcon icon={faCheck} className='register-form-icon'/>
                <input type='text' placeholder='confirm password...' ref={confirmPasswordInput}></input>
            </div>
            <div className='form-inner-container'>
                <p style={{margin: '0', color: 'red'}}>{errorMessage}</p>
            </div>
            <div className='login-form-footer'>
                <button type='button' onClick={register}>CREATE AN ACCOUNT</button>
            </div>
        </div>
    )
}

export default RegisterForm