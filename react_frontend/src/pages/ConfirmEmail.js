import React, {useEffect, useState, useContext} from "react";
import "./ConfirmEmail.css";
import {Context} from "../store/appContext";
import {useNavigate} from "react-router-dom";

function ConfirmEmail() {

    const navigate = useNavigate()
    const {store, actions} = useContext(Context)

    useEffect(() => {
       if(store.token || !store.emailToConfirm) navigate('/')
    }, [])

    return (
        <div className="login-container" style={{textAlign: 'center'}}>
            <div className="confirm-title">
                <h2>Verify your email address</h2>
                <h1>{store.emailToConfirm}</h1>
            </div>
        </div>
    )
}

export default ConfirmEmail