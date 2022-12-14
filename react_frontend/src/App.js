import React, {useState, useEffect} from "react";
import {Route, Routes, BrowserRouter} from "react-router-dom";
import Login from "./pages/Login";
import Home from "./pages/Home";
import injectContext from "./store/appContext";
import Register from "./pages/Register";
import ConfirmEmail from "./pages/ConfirmEmail";

function App() {

    return (
        <BrowserRouter>
            <Routes>
                <Route exact path='/' element={<Home/>}/>
                <Route exact path='/login' element={<Login/>}/>
                <Route exact path='/register' element={<Register/>}/>
                <Route exact path='/confirm' element={<ConfirmEmail/>}/>
            </Routes>
        </BrowserRouter>
    );
}

export default injectContext(App);
