import React, {useState, useRef} from 'react'
import '../css/ProductListModal.css'
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faPlus, faMinus, faXmark} from "@fortawesome/free-solid-svg-icons";
import Form from 'react-bootstrap/Form'
import DropdownButton from 'react-bootstrap/DropdownButton';
import DropdownItem from 'react-bootstrap/esm/DropdownItem';
import Dropdown from 'react-bootstrap/Dropdown';
import ProgressBar from './ProgressBar';

const ProductListModal = () => {

    const [show, setShow] = useState(false);
    const [quantity, setQuantity] = useState(1)
    const [productList, setProductList] = useState([])
    const [errorMessage, setErrorMessage] = useState(null)
    const [category, setCategory] = useState('All')
    const [searching, setSearching] = useState(false)

    const [progress, setProgress] = useState(0)

    const nameInput = useRef()
    const quantityInput = useRef()
    const categoryButton = useRef()

    console.log('ProductList rendered')

    const handleClose = () => setShow(false);
    const handleShow = () =>  {
        setQuantity(1)
        setProductList([])
        setCategory('All')
        setProgress(0)
        setShow(true)
        setSearching(false)
        setErrorMessage(null)
    }
    const increaseQuantity = () => {if (quantity < 10) setQuantity(quantity + 1)}
    const decreaseQuantity = () => {if (quantity > 0) setQuantity(quantity - 1)}

    const addProduct = () => {
        const product = nameInput.current.value
        const quantity = quantityInput.current.value
        if (product && !productList.some(item => item.product === product)) {
            setProductList([...productList, {
                product: product, 
                quantity: quantity
            }])
            setErrorMessage(null)
            console.log(productList)
        }
        else if(!product) setErrorMessage('Invalid name of the product')
        else setErrorMessage('Product is already in the list')
    }

    const deleteProduct = (product) => {
        setProductList(productList.filter(item => item.product !== product))
        setErrorMessage(null)
    }

    const submitListOfProducts = () => {
        if (productList.length === 0) {
            setErrorMessage('List of products is empty')
            return {"message": "List of products is empty"}
        }
        setErrorMessage(null)
        
        const mappedProductList = productList.map(item => item.product)
        const iterations = mappedProductList.length
        let currentIteration = 0
        mappedProductList.forEach(product => {
            console.log('WPISANY DO SCRAPERA', product)
            const options = {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    productList: [product],
                    category: category,
                })
            }
            console.log(options)
            setSearching(true)
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
                    currentIteration += 1
                    setProgress(Math.round(currentIteration / iterations * 100))
                    if (currentIteration === iterations) handleClose()
                })
                .catch(error => {
                    setErrorMessage("Server error")
                }) 
        })
    }
  
    return (
      <>
        <button className='product-list-modal-btn' onClick={handleShow}>
            Your product list
        </button>
        
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Search for best offers</Modal.Title>
            </Modal.Header>
            {searching ? <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', margin: '10% 0'}}><ProgressBar filled={progress}/></div> : <Modal.Body>
                <div style={{display: 'flex', justifyContent: 'center'}}>
                    <h1 style={{fontWeight: '300'}}>Enter the names of the products you are looking for</h1>
                </div>
                <div className='product-list-overflow'>
                    {productList.map((item, index) => {
                            return <div key={index} style={{display: "flex", alignItems: "center", justifyContent: 'space-between'}}>
                                <div style={{display: "flex", padding: "0.5%", whiteSpace: 'nowrap'}}>
                                    <p style={{textAlign: 'center', color: 'black', fontSize: '25px', fontWeight: '300', marginRight: '5%', marginBottom: '0'}}>name:</p>
                                    <p style={{textAlign: 'center', color: 'black', fontSize: '25px', fontWeight: '500', marginRight: '10%', marginBottom: '0'}}>{item.product}</p>
                                    <p style={{textAlign: 'center', color: 'black', fontSize: '25px', fontWeight: '300', marginRight: '5%', marginBottom: '0'}}>quantity:</p>
                                    <p style={{textAlign: 'center', color: 'black', fontSize: '25px', fontWeight: '400', marginRight: '10%', marginBottom: '0'}}>{item.quantity}</p>
                                </div>
                                <div style={{display: "flex", width: "100%", justifyContent: "end", alignItems: "center"}}>
                                    <button onClick={() => deleteProduct(item.product)}
                                    style={{background: "orange", border: "none", borderRadius: '60px', cursor: "pointer", padding: '1%', display: 'flex', alignItems: 'center'}}>
                                        <FontAwesomeIcon icon={faXmark}
                                        style={{objectFit: 'cover', height: '20px', width: '20px', margin: '0', padding: '0'}}/>
                                    </button>
                                </div>
                            </div>
                        })
                    }                   
                </div>
                <div className='product-list-form'>
                    <div className='product-section'>
                        <input type='text' placeholder='Name of the product...' id='product-name-input' ref={nameInput}></input>
                        <button type='button' onClick={increaseQuantity}>
                            <FontAwesomeIcon icon={faPlus} className='button-icon' style={{margin: '0', color: 'darkgreen'}}/>
                        </button>
                        <input type='text' value={quantity} readOnly={true} id='product-quantity-input' ref={quantityInput}></input>
                        <button type='button' onClick={decreaseQuantity}>
                            <FontAwesomeIcon icon={faMinus} className='button-icon' style={{margin: '0', color: 'darkred'}}/>
                        </button>
                        <button type='text' id='add-button' onClick={addProduct}>Add</button>
                    </div>
                    <div className='file-section'>
                    <Form.Group controlId="formFile" className="mb-3">
                        <div style={{display: 'flex', justifyContent: 'center'}}><Form.Label>Import list from file</Form.Label></div>
                        <Form.Control type="file" />
                    </Form.Group>
                    </div>
                </div>
                <p style={{color: 'red', margin: '0', height: '2vh'}}>{errorMessage}</p>
            </Modal.Body>
            }
            {searching ? null : <Modal.Footer>
                <button type='text' onClick={submitListOfProducts} id='search-button'>Search</button>
                <DropdownButton id="dropdown-item-button" title={category} ref={categoryButton}>
                    <Dropdown.Item as="button" onClick={() => {
                        setCategory('All')
                    }}>
                        All
                    </Dropdown.Item>
                    <Dropdown.Item as="button" onClick={() => {
                        setCategory('Health')
                    }}>
                        Health
                    </Dropdown.Item>
                    <Dropdown.Item as="button" onClick={() => {
                        setCategory('Beauty')
                    }}>
                        Beauty
                    </Dropdown.Item>
                </DropdownButton>
            </Modal.Footer>
            }
        </Modal>
        
      </>
    );
}

export default ProductListModal