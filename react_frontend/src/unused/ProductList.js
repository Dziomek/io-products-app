import './ProductList.css'
import React from "react";
import {useState, useRef} from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faMagnifyingGlass, faPlus, faXmark} from "@fortawesome/free-solid-svg-icons";
import DropdownButton from 'react-bootstrap/DropdownButton';
import DropdownItem from 'react-bootstrap/esm/DropdownItem';
import Dropdown from 'react-bootstrap/Dropdown';

function ProductList() {

    const [productList, setProductList] = useState([])
    const [errorMessage, setErrorMessage] = useState(null)
    const productInput = useRef()
    const categoryButton = useRef()

    const [category, setCategory] = useState('Wszystkie kategorie')

    const submitProduct = () => {
        const product = productInput.current.value
        if (product && !productList.includes(product)) {
            setProductList([...productList, product])
            setErrorMessage(null)
        }
        else if(!product) setErrorMessage('Invalid name of the product')
        else setErrorMessage('Product is already in the list')
    }

    const submitListOfProducts = () => {
        if (productList.length === 0) {
            setErrorMessage('List of products is empty')
            return {"message": "List of products is empty"}
        }
        setErrorMessage(null)

        const options = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                productList: productList,
                category: category,
            })
        }
        console.log(options)
        fetch("http://127.0.0.1:5000/scraping", options)
            .then(response => {
                console.log('Response status:', response.status)
                if (response.status !== 200) {
                    setErrorMessage("An error occured")
                }
                return response.json()
            })
            .then(data => {
                console.log(data)
            })
            .catch(error => {
                setErrorMessage("Server error")
            })
    }

    const deleteProductFromList = (product) => {
        setProductList(productList.filter(item => item !== product))
    }

    return (
        <div className="product-list-container">
            <div className="product-list-title">
                <h2>Create your own</h2>
                <h1>LIST OF PRODUCTS</h1>
                <h2>and search for</h2>
                <h1>BEST OFFERS</h1>
            </div>
            <div className="product-list">
                <div className="list-title">
                    <h1>Add products to the list</h1>
                </div>
                <div className="products-container">
                    {productList.map((product, index) => {
                        return <div key={index} style={{display: "flex", padding: "3px", alignItems: "center"}}>
                            <h3 className="added-product">{product}</h3>
                            <div style={{display: "flex", width: "100%", justifyContent: "end", alignItems: "center"}}>
                                <button onClick={() => deleteProductFromList(product)}
                                style={{background: "transparent", border: "none", cursor: "pointer"}}>
                                    <FontAwesomeIcon icon={faXmark} className="submit-list-icon"
                                    style={{color: "red"}}/>
                                </button>
                            </div>
                        </div>
                    })}
                </div>
                <div className="inner-container">
                    <div className="inner-secondary">
                       <input type="text" name="email" placeholder="product..." ref={productInput}/>
                        <button id="submit-product" onClick={submitProduct}>
                            <FontAwesomeIcon icon={faPlus} className="submit-icon"/>
                        </button>
                    </div>
                    <div className="inner-secondary" style={{color: "red", marginLeft: "10px"}}>
                        <h4>{errorMessage}</h4>
                    </div>
                    <div className="inner-secondary search">
                        <button id="submit-list" onClick={submitListOfProducts}>
                            <FontAwesomeIcon icon={faMagnifyingGlass} className="submit-list-icon"/>
                        </button>
                    </div>
                    <div>
                    <DropdownButton id="dropdown-item-button" title={category} ref={categoryButton}>
                    <Dropdown.Item as="button" onClick={() => {
                        setCategory('Wszystkie katerogie')
                    }}>
                        Wszystkie kategorie
                    </Dropdown.Item>
                    <Dropdown.Item as="button" onClick={() => {
                        setCategory('Zdrowie')
                    }}>
                        Zdrowie
                    </Dropdown.Item>
                    <Dropdown.Item as="button" onClick={() => {
                        setCategory('Uroda')
                    }}>
                        Uroda
                    </Dropdown.Item>
                    </DropdownButton>
                    </div>
                </div>
            </div>
        </div>
            )
}

export default ProductList