import React, {useState, useEffect} from "react";
import Navbar from "./components/Navbar";
import {Route, Routes} from "react-router-dom";
import Login from "./pages/Login";
import Home from "./pages/Home";

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
        <Routes>
            <Route exact path='/' element={<Home/>}/>
            <Route exact path='/login' element={<Login/>}/>
        </Routes>
    );
}

export default App;
