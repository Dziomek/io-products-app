import { React, useRef, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import '../css/Products.css'
import { faMagnifyingGlass, faShoppingCart } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from 'react-router-dom';
import { DropdownButton, Dropdown } from 'react-bootstrap';

const Products = () => {

    const navigate = useNavigate()
    const productInput = useRef()
    const location = useLocation()
    const productLists = location.state && location.state.productLists
    const [errorMessage, setErrorMessage] = useState(null)
    const [selectedItems, setSelectedItems] = useState([]);

    
    
    console.log('Products page rendered. Searched items:', productLists, 'selected:', selectedItems)

    const handleChange = (index, value) => {
        const newSelectedItems = [...selectedItems];
        newSelectedItems[index] = value;
        setSelectedItems(newSelectedItems);
    };
    const allChecked = () => {
        let validLength = 0
        productLists.forEach(item => {
            if (item.productList.length !== 0) validLength += 1
        })
        console.log('Valid length: ', validLength)
        
        return selectedItems.filter(element => element !== undefined && element !== null && element !== "").length === validLength
    }
    const handleSubmit = () => {
            // fetch("http://127.0.0.1:5000/list", {
            // method: 'POST',
            // headers: { 'Content-Type': 'application/json' },
            // body: JSON.stringify({ data: selectedItems })
            // })
            // .then(response => response.json())
            // .then(data => {
            //     console.log("data send to api:",data);
            // })
            // .catch(error => {
            //     console.error(error);
            // })
            const nameList = selectedItems.filter(element => element !== undefined && element !== null && element !== "")
            console.log(nameList)
            const results = productLists.map(element => {
                let filteredProducts = element.productList.filter(product => nameList.includes(product.name));
                if (filteredProducts.length > 0) {
                    return {
                        ...element,
                        productList: filteredProducts
                    }
                }
            }).filter(element => element !== undefined && element !== null && element !== "")
            navigate('/summary', { state: { productLists: results }})
        }

    function submitProductFromList(productName){
        const receivedProductLists = []
        
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
    

    const submitProduct = () => {
        const receivedProductLists = []
        const productName = productInput.current.value

        if (!productName) {
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
                navigate('/products', {
                    state: {
                        productLists: receivedProductLists
                    }
                })
            })
            .catch(error => {
                setErrorMessage("Server error")
            })
    }

    // console.log('Products rendered. ProductsList: ', productLists)
    // console.log('selected items', selectedItems)

    return (
        <body style={{backgroundColor: '#f2f5f7',backgroundImage:'none',backgroundSize:'cover'}}>  
        <div style={{backgroundColor: '#f2f5f7',backgroundImage:'none',backgroundSize:'cover'}}>
            <div className='title-container-products'>
                <Link style={{textDecoration: 'none'}} to='/'>
                    <h1 >PRODUCTS <h1 className="title-2nd-part">APP</h1></h1>
                </Link>
                <input type="text" placeholder="Type in product name" ref={productInput} />
                <button className="search-btn-products" onClick={submitProduct}>Search</button>
            </div>
            {productLists ?
                <>
                    {
                        productLists.map((object, index) => {
                            return <div key={index} style={{backgroundColor:'#f2f5f7'}}>                              
                                {object.productList.length > 1 && <>
                                    <h3 className='search-result' style={{backgroundColor:'#f2f5f7'}}>Wyniki wyszukiwania dla: {object.searchedProduct}</h3>
                                    <div className='products-container'>
                                        {object.productList.map((product, secondIndex) => {
                                            return <div className='product_container' key={secondIndex} style={{ marginBottom: '2%' }}>
                                                <img src={product.image} alt='Product'></img>
                                                <div className='product-name'>{product.name }</div>
                                                <div className='product-price'>Cena: {product.price}zł</div>
                                                {isNaN(parseFloat(product.deliveryprice)) ?
                                                <div className='product-price'> Cena dostawy nieznana</div>
                                                :
                                                <div className='product-price'>Z dostawą: {String((parseFloat(product.price.replace(/,/g, '.'))+parseFloat(product.deliveryprice)).toFixed(2)).replace(/\./g,",")} zł</div>
                                                }
                                                <button onClick={()=>{submitProductFromList(product.name)}}>Sprawdź</button>
                                                <input 
                                                type='radio'
                                                name={`product-${index}-${secondIndex}`}
                                                value={product.name}
                                                checked={selectedItems[index] === product.name}
                                                onChange={()=>handleChange(index, product.name)}
                                                ></input>


                                            </div>
                                        })}
                                        </div>
                                    
                                </>}
                                
                                {object.productList.length === 1 && <>
                                    <h3 className='search-result'>Wyniki wyszukiwania dla: {object.searchedProduct}</h3>
                                    <div>
                                        {object.productList.map((product, secondIndex) => {
                                            return <div className='single-product-container'  key={secondIndex} style={{ marginBottom: '2%' }}>
                                                <img src={product.image} alt='Product'></img>
                                                <div className='product-top-name'>
                                                    <h5>{product.name}</h5>
                                                    {isNaN(parseFloat(product.deliveryprice)) ?
                                                    <div className='product-price'> Cena dostawy nieznana</div>
                                                    :
                                                    <h6>Delivery price: {String(product.deliveryprice.toFixed(2)).replace(/\./g,",")}zł</h6>
                                                    }   
                                                    <a href={product.link}>Link do sklepu</a>
                                                </div>
                                                <div className='price-add-container'>    
                                                    <h3>{product.price}zł</h3>
                                                    <button onClick={()=>handleChange(index ,product.name)}>Dodaj</button>
                                                    <p>With ship {String((parseFloat(product.price.replace(/,/g, '.'))+parseFloat(product.deliveryprice)).toFixed(2)).replace(/\./g,",")} zł</p>
                                                </div>
                                            </div>
                                        })}
                                    </div>
                                </>}
                                {object.productList.length === 0 && 
                                <>
                                    <h3 className='search-result'>Nie udało się znaleźć produktów dla: {object.searchedProduct}</h3>
                                </>

                                }

                            </div>
                        })
                    }
                </>
                :
                <>
                    <h1>PUSTA LISTA PRODUKTÓW</h1>
                </>
            }
        <button disabled={!allChecked()} onClick={handleSubmit}className='finish-btn'><FontAwesomeIcon className='cart-icon' icon={faShoppingCart}></FontAwesomeIcon></button>
        </div>
        </body>
    )
}

export default Products