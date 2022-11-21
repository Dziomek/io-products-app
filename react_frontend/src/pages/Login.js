import './Login.css'
import {useEffect, useState, useContext} from "react";
import {useNavigate} from 'react-router-dom'
import {Context} from "../store/appContext";

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
                <h1>Test login page</h1>
                <input type="text" name="email" placeholder="email" onChange={
                    (e) => setEmail(e.target.value)}/>
                <input type="password" name="password" placeholder="password" onChange={
                    (e) => setPassword(e.target.value)}/>
                <button type="submit" onClick={handleClick}>Login</button>
            </div>
        </>
    )
}

export default Login