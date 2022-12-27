import React, {useEffect, useState, useContext} from "react";
import "../css/ConfirmEmail.css";
import {Context} from "../store/appContext";
import {useNavigate} from "react-router-dom";

function ConfirmEmail() {
    const navigate = useNavigate()
    const {store, actions} = useContext(Context)
    const [email, setEmail] = useState(null)

    useEffect(() => {
        actions.syncDataFromSessionStorage()
        setEmail(store.emailToConfirm)
        if(store.token || !store.emailToConfirm && store.is_active !== false) {
            actions.removeStoreData()
            navigate('/')
        }
        actions.removeStoreData()
        console.log('Store deleted')
    }, [])

    function handleReturn() {
        sessionStorage.removeItem("emailToConfirm")
        navigate('/login')
    }

    return (
        <div className="login-container" style={{textAlign: 'center'}}>
            <div className="confirm-title">
                <h2>Verify your email address</h2>
                <h3>We have sent an activation link to your e-mail address</h3>
                <h4>{email}</h4>
                <div className="inner-container">
                    <button id="return-button" onClick={handleReturn}>Return to login page</button>
                </div>
            </div>
        </div>
    )
}

export default ConfirmEmail