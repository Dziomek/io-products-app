import './Login.css'
import {useEffect, useState} from "react";
import {useNavigate} from 'react-router-dom'

function Login() {
    const navigate = useNavigate()
    const [token, setToken] = useState(sessionStorage.getItem("token"))
    const [email, setEmail] = useState(null)
    const [password, setPassword] = useState(null)

    useEffect(() => {
        if (token) navigate('/')
    }, [token])

    const handleClick = () => {
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

        fetch("http://127.0.0.1:5000/token", options)
            .then(response => {
                if(response.status === 200) return response.json()
                else alert("An error occured")
            })
            .then(data => {
                sessionStorage.setItem("token", data.access_token)
                setToken(data.access_token)
                console.log(data.access_token)
            })
            .catch(error => {
                console.error("An error occured")
            })
    }

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