import React from "react";
import {useNavigate} from "react-router-dom";
import {useContext, useEffect, useState, useRef} from "react";
import {Context} from "../store/appContext";
import './Register.css'


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
                if(data.message === "User succesfully created") navigate('/login')
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


    return(
        <>
            <div className='login-container'>
                <div className="login-title">
                    <h2>Create new</h2>
                    <h1>ACCOUNT</h1>
                </div>
                <div className="login-form">
                    <div className="error-container">
                        <p>{errorMessage}</p>
                    </div>
                    <div className="inner-container input">
                        <input type="username" name="username" placeholder="username" ref={usernameInput}/>
                    </div>
                    <div className="inner-container input">
                        <input type="text" name="email" placeholder="email" ref={emailInput}/>
                    </div>
                    <div className="inner-container input">
                        <input type="password" name="password" placeholder="password" ref={passwordInput}/>
                    </div>
                    <div className="inner-container input">
                        <input type="password" name="confirm-password" placeholder="confirm password" ref={confirmPasswordInput}/>
                    </div>
                    <div className="spacer"></div>
                    <div className="inner-container">
                        <button type="submit" onClick={submitRegistration}>Register</button>
                    </div>
                </div>
            </div>
        </>
    )
}
export default Register