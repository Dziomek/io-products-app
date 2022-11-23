import React from "react";
import {useNavigate} from "react-router-dom";
import {useContext, useEffect, useState, useRef} from "react";
import {Context} from "../store/appContext";


function Register() {
    const navigate = useNavigate()
    const {store, actions} = useContext(Context)

    const emailInput = useRef()
    const passwordInput = useRef()

    const submitRegistration = () => {
        const email = emailInput.current.value
        const password = passwordInput.current.value

        console.log('email', email, 'password', password)

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
        fetch("http://127.0.0.1:5000/register_user", options)
            .then(response => {
                if(response.status === 200) return response.json()
                else alert("An error occured")
            })
            .then(data => {
                console.log(data)
                if(data.message === "User succesfully created") navigate('/login')
            })
            .catch(error => {
                console.error("An error occured")
            })
    }

    useEffect(() => {
        console.log('TOKEN', store.token)
        if(store.token) navigate('/')
    }, [store.token])

    return(
        <>
            <div className='login-container'>
                <div className="login-form" >
                    <div className="form-icon">
                        <img src={require('../images/user-icon.png')} alt=""/>
                    </div>
                    <div className="inner-container input">
                        <input type="text" name="email" placeholder="email" ref={emailInput}/>
                    </div>
                    <div className="inner-container input">
                        <input type="password" name="password" placeholder="password" ref={passwordInput}/>
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