import React, {useState, useEffect} from "react";
import {Route, Routes, BrowserRouter} from "react-router-dom";
import Login from "./pages/Login";
import Home from "./pages/Home";
import injectContext from "./store/appContext";
import Register from "./pages/Register";

function App() {
    const [data, setData] = useState([])

    useEffect(() => {
        fetch("http://127.0.0.1:5000").then(
            r => r.json()).then(
            data => {
            setData(data)
            console.log(data)
          })
    }, [])

    return (
        <BrowserRouter>
            <Routes>
                <Route exact path='/' element={<Home/>}/>
                <Route exact path='/login' element={<Login/>}/>
                <Route exact path='/register' element={<Register/>}/>
            </Routes>
        </BrowserRouter>
    );
}

export default injectContext(App);
