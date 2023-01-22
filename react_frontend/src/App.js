import React, {useState, useEffect, useContext} from "react";
import {Route, Routes, BrowserRouter} from "react-router-dom";
import Login from "./unused/Login";
import Home from "./pages/Home";
import injectContext, { Context } from "./store/appContext";
import Register from "./unused/Register";
import ConfirmEmail from "./unused/ConfirmEmail";
import Products from "./pages/Products";
import History from "./pages/History";
import SelectedProducts from "./pages/SelectedProducts";

function App() {

    console.log('App rendered')

    return (
        <BrowserRouter>
            <Routes>
                <Route exact path='/' element={<Home/>}/>
                {/* <Route exact path='/login' element={<Login/>}/>
                <Route exact path='/register' element={<Register/>}/> */}
                {/* <Route exact path='/confirm' element={<ConfirmEmail/>}/> */}
                <Route exact path='/products' element={<Products/>}/>
                <Route exact path='/history' element={<History/>}/>
                <Route exact path='/summary' element={<SelectedProducts/>}/>
            </Routes>
        </BrowserRouter>
    );
}

export default injectContext(App);
