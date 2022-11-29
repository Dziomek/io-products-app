import './ProductList.css'
import React from "react";
import {useState, useRef} from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faMagnifyingGlass, faPlus} from "@fortawesome/free-solid-svg-icons";

function ProductList() {

    const [productList, setProductList] = useState([])
    const productInput = useRef()

    const submitProduct = () => {
        const product = productInput.current.value
        if (product) setProductList([...productList, product])
        console.log(productList)
    }

    const submitListOfProducts = () => {
        console.log(productList)
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
                        return <div key={index} style={{display: "flex"}}>
                            <h3 className="added-product">{product}</h3>
                            <button>Remove</button>
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
                    <div className="inner-secondary search">
                        <button id="submit-list" onClick={submitListOfProducts}>
                            <FontAwesomeIcon icon={faMagnifyingGlass} className="submit-list-icon"/>
                        </button>
                    </div>
                </div>
            </div>
        </div>
            )
}

export default ProductList