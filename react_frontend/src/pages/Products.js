import {React,useRef, useState} from 'react'
import { useLocation,useNavigate } from 'react-router-dom'
import '../css/Products.css'
import {faMagnifyingGlass} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";



const Products = () => {
    
    const navigate = useNavigate()
    const productInput = useRef()
    const location = useLocation()
    const productLists = location.state && location.state.productLists
    const [errorMessage, setErrorMessage] = useState(null)

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
    
    console.log('Products rendered. ProductsList: ', productLists)
    
    return (
        <div>
            <div className='title-container-products'>
             <h1 >PRODUCTS <h1 className="title-2nd-part">APP</h1></h1>
             <input type="text" placeholder="Type in product name" ref={productInput}/>
             <button className="search-btn-products" onClick={submitProduct}>Search</button>

             </div>
            { productLists ? 
            <>
            {
                productLists.map((object, index) => {
                    return <div  key={index}>
                    <h3 className='search-result'>Wyniki wyszukiwania dla: {object.searchedProduct}</h3>
                    <div className='products-container'>
                    {object.productList.map((product, secondIndex) => {
                        return <div className='product_container' key={secondIndex} style={{marginBottom: '2%'}}>
                            <img src={product.image} alt='Product'></img>
                            <div className='product-name'>{product.name}</div>
                            <div className='product-price'>{product.price}zł</div>
                                <button>Add to list</button>
                            </div>
                    })}</div>
                    </div>
                })
            }
            </>
            :
            <>
                <h1>PUSTA LISTA PRODUKTÓW</h1>
            </>
            }
            
        </div>
    )
}

export default Products