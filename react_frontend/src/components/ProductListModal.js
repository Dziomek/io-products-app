import React, {useState, useRef, useEffect, useContext} from 'react'
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
import { useNavigate } from 'react-router-dom';
import Papa from "papaparse";
import { Context } from '../store/appContext';

const ProductListModal = () => {

    const {store, actions} = useContext(Context)
    const [show, setShow] = useState(false);
    const [quantity, setQuantity] = useState(1)
    const [productList, setProductList] = useState([])
    const [errorMessage, setErrorMessage] = useState(null)
    const [category, setCategory] = useState('All')
    const [searching, setSearching] = useState(false)
    const [csvFile, setCsvFile] = useState(null)
    const [allegro, setAllegro] = useState(false)
    const [deliveryPrice, setDeliveryPrice] = useState(true)
    const [fileErrorMessage, setFileErrorMessage] = useState(null)
    const [sortByShops, setSortByShops] = useState(false)

    const [progress, setProgress] = useState(0)

    const nameInput = useRef()
    const quantityInput = useRef()
    const fileInput = useRef()
    const allowedExtensions = ["csv"];
    const categoryButton = useRef()

    const navigate = useNavigate()

    console.log('ProductList rendered. Current csv file: ', csvFile, typeof csvFile)

    const handleFileUpload = async (event) => {
        event.preventDefault()
        setFileErrorMessage(null)
        const file = event.target.files[0]
        if(file && file.name.split('.').pop() !== 'csv'){
            fileInput.current.value = null
            setFileErrorMessage('Invalid file type. Please upload a CSV file')
            return
        }
        fileInput.current.value = null
        setCsvFile(file)
    }

    useEffect(() => {
        if (!csvFile) return

        setProductList([])

        Papa.parse(csvFile, {
            header: true,
            complete: (results) => {
                const newProductList = results.data.map(row => {
                    return {
                        product: row.name,
                        quantity: 1
                    }
                });
                setProductList(prevProductList => [...prevProductList, ...newProductList])
            }
        });
        setCsvFile(null)
    }, [csvFile]);


    const handleClose = () => setShow(false);
    const handleShow = () =>  {
        setQuantity(1)
        setProductList([])
        setCategory('All')
        setProgress(0)
        setShow(true)
        setSearching(false)
        setErrorMessage(null)
        setCsvFile(null)
        setAllegro(false)
        setFileErrorMessage(null)
    }
    const increaseQuantity = () => {if (quantity < 10) setQuantity(quantity + 1)}
    const decreaseQuantity = () => {if (quantity > 0) setQuantity(quantity - 1)}

    const addProduct = () => {
        const product = nameInput.current.value
        // const quantity = quantityInput.current.value
        if (product && !productList.some(item => item.product === product)) {
            setProductList([...productList, {
                product: product, 
                quantity: 1
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

    // const uploadFile = (event) => {
    //     const inputFile = event.target.files[0];
    //     // todo: validate file extension
    //     setFile(inputFile);
    //     console.log(inputFile)

    //     Papa.parse(inputFile, {
    //         header: true,
    //         skipEmptyLines: true,
    //         complete: function (results) {
    //             const rowsArray = [];
    //             const valuesArray = [];
    //             results.data.map((d) => {
    //                 rowsArray.push(Object.keys(d));
    //                 valuesArray.push(Object.values(d));
    //             })
    //             setParsedData(results.data);
    //             setTableRows(rowsArray[0]);
    //             setValues(valuesArray);
    //             console.log(parsedData)
    //             console.log(values)

    //         },
    //     })
    //     // const reader = new FileReader();
    //     // reader.onload = async ({ target }) => {
    //     // const csv = Papa.parse(target.result, { header: true });
    //     // const parsedData = csv?.data;
    //     // const columns = Object.keys(parsedData[0]);
    //     // setData(columns);
    //     // }
    //     // reader.readAsText(file)
    // }

    const submitListOfProducts = () => {
        const receivedProductLists = []

        if (productList.length === 0) {
            setErrorMessage('List of products is empty')
            return {"message": "List of products is empty"}
        }
        setErrorMessage(null)
        
        const mappedProductList = productList.map(item => item.product)
        const iterations = mappedProductList.length
        let currentIteration = 0
        mappedProductList.forEach(product => {
            // console.log('WPISANY DO SCRAPERA', product)
            const options = {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    productList: [product],
                    category: category,
                    quantity: mappedProductList.length,
                    allegro: allegro,
                    deliveryPrice: deliveryPrice,
                    sortByShops: sortByShops,
                    count: iterations
                })
            }
            console.log(options)
            setSearching(true)
            fetch("http://10.160.73.81:5000/scraping", options)
                .then(response => {
                    console.log('Response status:', response.status)
                    if (response.status !== 200) {
                        setErrorMessage("An error occured")
                    }
                    return response.json()
                })
                .then(data => {
                    console.log('TO OTRZYMALEM NAJPIERW Z BACKENDU', data)
                    const shops = data.shops
                    console.log('INFO O FLADZE SHOPS', shops, shops ? 'jest flaga' : 'nie ma flagi')
                    currentIteration += 1
                    setProgress(Math.round(currentIteration / iterations * 100))
                    if (data.timeout) receivedProductLists.push({
                        searchedProduct: product,
                        category: category,
                        productList: [],
                        timeout: data.timeout
                    }) 
                    else receivedProductLists.push({
                        searchedProduct: product,
                        category: category,
                        productList: data.product_list.items,
                        timeout: false 
                    })
                    console.log(receivedProductLists)
                    if (currentIteration === iterations) {
                        handleClose()
                        console.log('TO SOBIE OGARNALEM', receivedProductLists)
                        if (shops) {
                            navigate('/summary', {state: { 
                                productLists: [receivedProductLists[receivedProductLists.length - 1]]
                            }}) 
                            return
                        }
                        navigate('/products', {state: { 
                                productLists: receivedProductLists
                            }})
                    }
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
                                    {/* <p style={{textAlign: 'center', color: 'black', fontSize: '25px', fontWeight: '300', marginRight: '5%', marginBottom: '0'}}>quantity:</p>
                                    <p style={{textAlign: 'center', color: 'black', fontSize: '25px', fontWeight: '400', marginRight: '10%', marginBottom: '0'}}>{item.quantity}</p> */}
                                </div>
                                <div style={{display: "flex", width: "100%", justifyContent: "end", alignItems: "center"}}>
                                    <button onClick={() => deleteProduct(item.product)}
                                    style={{background: "#f5c422", border: "none", borderRadius: '8px', cursor: "pointer", padding: '0.5%', display: 'flex', alignItems: 'center'}}>
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
                        {/* <button type='button' onClick={increaseQuantity}>
                            <FontAwesomeIcon icon={faPlus} className='button-icon' style={{margin: '0', color: 'darkgreen'}}/>
                        </button>
                        <input type='text' value={quantity} readOnly={true} id='product-quantity-input' ref={quantityInput}></input>
                        <button type='button' onClick={decreaseQuantity}>
                            <FontAwesomeIcon icon={faMinus} className='button-icon' style={{margin: '0', color: 'darkred'}}/>
                        </button> */}
                        <button type='text' id='add-button' onClick={addProduct}>Add</button>
                    </div>
                    <div className='file-section'>
                    <Form.Group controlId="formFile" className="mb-3">
                        <div style={{display: 'flex', justifyContent: 'center'}}><Form.Label>Import list from file</Form.Label></div>
                        <Form.Control type="file" ref={fileInput} onChange={handleFileUpload}/>
                        <p style={{color: 'red'}}>{fileErrorMessage}</p>
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
                <Form>
                    <Form.Check 
                        type="switch"
                        id="custom-switch"
                        label="Allegro only"
                        checked={allegro}
                        onChange={() => {
                            if (!allegro) {
                                setAllegro(true)  
                                setSortByShops(false)
                            } 
                            else setAllegro(false)
                        }}
                        disabled={sortByShops}
                    />
                    <Form.Check 
                        type="switch"
                        id="custom-switch"
                        label="Do not include delivery price"
                        onChange={() => {
                            if (deliveryPrice) setDeliveryPrice(false)
                            else setDeliveryPrice (true)
                        }}
                    />
                    <Form.Check 
                        type="switch"
                        id="custom-switch"
                        label="Sort by shops"
                        checked={sortByShops}
                        onChange={() => {
                            if (sortByShops) setSortByShops(false)
                            else {
                               setSortByShops(true) 
                               setAllegro(false)
                            } 
                        }}
                        disabled={allegro}
                    />
                </Form>
            </Modal.Footer>
            }
        </Modal>
        
      </>
    );
}

export default ProductListModal