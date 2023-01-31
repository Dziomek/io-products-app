import React, { useState, useEffect, useContext } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { Context } from '../store/appContext'
import Form from 'react-bootstrap/Form'
import '../css/SelectedProducts.css'
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { NavItem } from 'react-bootstrap'
import { Link } from 'react-router-dom'



const SelectedProducts = () => {
    
    const {store, actions} = useContext(Context)
    const location = useLocation()
    const navigate = useNavigate()
    const [totalPrice, setTotalPrice] = useState(0);
    const [value, setValue] = useState(1)

    const [show, setShow] = useState(false);    
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const [productLists, setProductLists] = useState(location.state && location.state.productLists.map(element => {
        return element.productList
    }).flat())
    const [selectedValues, setSelectedValues] = useState(productLists.map(item =>{
        return 1;
    }));

    
  


    const calculateTotalPrice = () => {
    
        if(value===1){ const total = productLists.reduce((acc, product, index) => {
            return acc + (parseFloat(product.price.replace(/,/g, '.'))+parseFloat(product.deliveryprice !== "" ? product.deliveryprice : 0))
        }, 0)
        setTotalPrice(total);}
        else{const total = productLists.reduce((acc, product, index) => {
            return acc + (parseFloat(product.price.replace(/,/g, '.'))*parseFloat(selectedValues[index])+parseFloat(product.deliveryprice !== "" ? product.deliveryprice : 0))
        }, 0)
        setTotalPrice(total);}
    }
    useEffect(() => {
        calculateTotalPrice();
    }, [selectedValues])

    const handleChange = (event, index) => {
        setValue(2);
        let newSelectedValues = [...selectedValues];
        newSelectedValues[index] = event.target.value;
        setSelectedValues(newSelectedValues);
    }

    
    console.log('SelectedProducts rendered. ProductLists: ', productLists)

    useEffect(() => {
        if (!productLists) {
            navigate('/')
            return
        }
    }, [])

    const handleSubmit = () => {
        let modifiedProductLists = productLists.map((product, index) => {
            return {...product, totalPrice: parseFloat(product.price.replace(/,/g, '.'))*parseFloat(selectedValues[index])+parseFloat(product.deliveryprice)}
        })
        const options = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: store.id, 
                productLists: modifiedProductLists
            })
        }
        console.log(options)
        fetch("http://127.0.0.1:5000/save", options)
            .then(res => {
                if (res.status === 200) return res.json()
            })
            .then(data => {
                console.log(data)
            })
            setShow(false)
            navigate('/')
    }
    console.log(selectedValues)
    return (
        <>
        <body style={{backgroundColor: '#f2f5f7',backgroundImage:'none'}}>
        <div className='title-container-products' style={{marginBottom: '30px'}}>
                <Link style={{textDecoration: 'none'}} to='/'>
                    <h1 >PRODUCTS <h1 className="title-2nd-part">APP</h1></h1>
                </Link>
                {/* <input type="text" placeholder="Type in product name" ref={productInput} />
                <button className="search-btn-products" onClick={submitProduct}>Search</button> */}
        </div>
            {productLists.map((product, index) => {
                return <div style={{backgroundColor: '#f2f5f7'}}key={index}>
                <div className='single-product-container-picked' style={{ marginBottom: '2%', }}>
                    <img src={product.image} alt='Product'></img>
                    <div className='product-top-name'>
                        <h5>{product.name}</h5>
                        {isNaN(parseFloat(product.deliveryprice)) ?
                        <h6> Cena dostawy nieznana</h6>
                        :
                        <h6>Delivery price: {String(product.deliveryprice.toFixed(2)).replace(/\./g,",")}zł</h6>
                        }
                        <a href={product.link}>Link to the shop</a>
                        <p>{product['shop name']}</p>
                    </div>
                    <div className='price-add-container'>    
                        <h3>{product.price}zł</h3>
                        <Form.Select className='select' defaultValue={1} onChange={(event)=>{handleChange(event, index)}}>
                                                        <option value="1">1</option>
                                                        <option value="2">2</option>
                                                        <option value="3">3</option>
                                                        <option value="5">5</option>
                                                        <option value="10">10</option>
                                                        <option value="20">20</option>
                                                </Form.Select>                                                 
                        {value===1 ? 
                        <p >With ship  {String((parseFloat(product.price.replace(/,/g, '.')) + 
                        parseFloat(product.deliveryprice !== "" ? product.deliveryprice : 0)).toFixed(2)).replace(/\./g,",")} zł</p>
                        :
                        <p >With ship  {String((parseFloat(product.price.replace(/,/g, '.')) * 
                        parseFloat(selectedValues[index])+parseFloat(product.deliveryprice !== "" ? product.deliveryprice : 0)).toFixed(2)).replace(/\./g,",")} zł</p>
                        }
                    </div>
                </div>
            </div>
        
            })}
            { !store.token ?
            
            <div style={{backgroundColor: '#f2f5f7', display: 'flex', justifyContent: 'center'}}>
            <p style={{fontSize: '30px'}}>Total price: <b>{String(totalPrice.toFixed(2)).replace(/\./g,",")} zł</b></p>   
            </div>
            
            :<>
            <div style={{backgroundColor: '#f2f5f7', display: 'flex', justifyContent: 'center'}}>
            <p style={{fontSize: '30px'}}>Total price: {String(totalPrice.toFixed(2)).replace(/\./g,",")} zł</p>   
            
            </div>
            <div style={{display: 'flex', justifyContent: 'center'}}>
                <Button style={{backgroundColor:'orange', border:'none'}} onClick={handleShow}>
                    Zatwierdź
                </Button>
            </div>

                <Modal show={show} onHide={handleClose} animation={false}>
                    <Modal.Header closeButton>
                        <Modal.Title>Podsumowanie</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>Czy na pewno chcesz zatwierdzić listę?</Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={handleClose}>
                            Zamknij
                        </Button>
                        <Button style={{backgroundColor:'orange'}}  onClick={handleSubmit}>
                            Zatwierdź
                        </Button>
                    </Modal.Footer>
                </Modal>
            </>
            }
            </body>
        </>
    )
}

export default SelectedProducts