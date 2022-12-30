import React, {useContext, useState, useEffect, useRef} from 'react'
import { Context } from '../store/appContext'
import '../css/LoginAndRegisterForm.css'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faKey, faEnvelope, faUser, faCheck} from '@fortawesome/free-solid-svg-icons'
import ConfirmEmailModal from './ConfirmEmailModal';

const RegisterForm = () => {
    
    const {store, actions} = useContext(Context)
    const [errorMessage, setErrorMessage] = useState(null)
    const [registered, setRegistered] = useState(false)
    const [email, setEmail] = useState(null)

    const emailInput = useRef()
    const passwordInput = useRef()
    const usernameInput = useRef()
    const confirmPasswordInput = useRef()

    console.log('RegisterForm rendered. registered: ', registered)
    
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
                    setEmail(email)
                    setRegistered(true)
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
            {!registered ? 
            <>
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
                    <input type='password' placeholder='confirm password...' ref={confirmPasswordInput}></input>
                </div>
                <div className='form-inner-container'>
                    <p style={{margin: '0', color: 'red'}}>{errorMessage}</p>
                </div>
                <div className='login-form-footer'>
                    <button type='button' onClick={register}>CREATE AN ACCOUNT</button>
                </div>
            </> 
            :
            <>
                <ConfirmEmailModal email={email}/>
                <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                    <button style={{width: '30%', borderRadius: '30px', backgroundColor: 'orange', border: 'none', fontSize: '20px'}} onClick={() => setRegistered(false)}>Return</button>
                </div>
            </>
            }
        </div>
    )
}

export default RegisterForm