import {useContext, useEffect, useRef, useState} from "react";
import {Context} from "../store/appContext";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faMagnifyingGlass} from '@fortawesome/free-solid-svg-icons'
import ProductListModal from "../components/ProductListModal";
import LoginRegisterModal from "../components/LoginRegisterModal";
import '../css/Home.css'
import { Link, useNavigate } from "react-router-dom";

function Home() {

    const {store, actions} = useContext(Context)
    const [errorMessage, setErrorMessage] = useState(null)

    const productInput = useRef()
    const navigate = useNavigate()

    const submitProduct = () => {
        const receivedProductLists = []
        const productName = productInput.current.value

        if(!productName) {
            setErrorMessage('Type in product name')
            return
        }
        
        setErrorMessage(null)
        const options = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                productList: [productName],
                category: 'All',
            })
        }

        fetch("http://127.0.0.1:5000/scraping", options)
            .then(response => {
                console.log('Response status:', response.status)
                if (response.status !== 200) {
                    setErrorMessage("An error occured")
                }
                return response.json()
            })
            .then(data => {
                receivedProductLists.push({
                    searchedProduct: productName,
                    category: 'All',
                    productList: data.product_list.items
                })
                console.log(data)
                navigate('/products', {state: { 
                        productLists: receivedProductLists
                    }})
                })
            .catch(error => {
                setErrorMessage("Server error")
            }) 
    }

    console.log('Home rendered', store.token)

    return (
        <>
        <div className="title-container">
            <h1 >PRODUCTS <h1 className="title-2nd-part">APP</h1></h1>
            { !store.token ?
                <div className="login-container">
                    <LoginRegisterModal/>
                </div>
                :
                <div className="login-container">
                    <h1>{store.username}</h1>
                    <button onClick={() => actions.logout()}>Log out</button>
                    <Link to='/history'>History</Link>
                </div>
            }        
        </div>
        <div className="search-bar-container">
            <h1>The best deals for You.</h1>
            <div className="search-bar-inner-container">
            <FontAwesomeIcon className='icon' icon={faMagnifyingGlass}/>
                <input type="text" placeholder="Type in product name" ref={productInput}/>
            </div>
            <button className="search-btn" onClick={submitProduct}>Search</button>
            <ProductListModal/>
        </div>
        {errorMessage}
        <a className="log-in-a">Log in</a><p className="log-in-paragraph"> to save your lists.</p>
        </>
    )
}

export default Home