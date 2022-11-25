import './Login.css'
import {useEffect, useState, useContext} from "react";
import {useNavigate} from 'react-router-dom'
import {Context} from "../store/appContext";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import { faEnvelope } from '@fortawesome/free-regular-svg-icons'

function Login() {
    const navigate = useNavigate()
    const {store, actions} = useContext(Context)
    const [email, setEmail] = useState(null)
    const [password, setPassword] = useState(null)

    const handleClick = () => {
        actions.login(email, password)
        console.log(store.token)
    }

    useEffect(() => {
        console.log(store.token)
        if(store.token) navigate('/')
    }, [store.token])

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
                    <div className="inner-container input">
                        <FontAwesomeIcon icon={faEnvelope}/>
                        <input type="text" name="email" placeholder="email" onChange={
                            (e) => setEmail(e.target.value)}/>
                    </div>
                    <div className="inner-container input">
                        <input type="password" name="password" placeholder="password" onChange={
                                (e) => setPassword(e.target.value)}/>
                    </div>
                    <div className="spacer"></div>
                    <div className="inner-container">
                        <button type="submit" onClick={handleClick}>Log in</button>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Login