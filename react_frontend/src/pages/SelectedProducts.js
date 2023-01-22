import React, { useState, useEffect, useContext } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { Context } from '../store/appContext'
import Form from 'react-bootstrap/Form'
import '../css/SelectedProducts.css'


const SelectedProducts = () => {
    
    const {store, actions} = useContext(Context)
    const location = useLocation()
    const navigate = useNavigate()
    const [selectedValue, setSelectedValue] = useState('1');
    const [productPrice, setProductPrice] = useState(null)

    const handleChange = (event, index) => {
        setSelectedValue(event.target.value);
        setProductPrice(productLists[index].price)
      }

    const [productLists, setProductLists] = useState(location.state && location.state.productLists.map(element => {
        return element.productList
    }).flat())
    
    console.log('SelectedProducts rendered. ProductLists: ', productLists)

    useEffect(() => {
        if (!productLists) {
            navigate('/')
            return
        }
    }, [])

    const handleSubmit = () => {
        productLists.forEach(product => {
            const options = {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    id: store.id, 
                    link: product.link,
                    name: product.name,
                    price: product.price
                })
            }
            console.log(options)
            fetch("http://127.0.0.1:5000/save", options)
                .then(res => {
                    if (res.status === 200) return res.json()
                })
                .then(data => {
                    console.log(data)
                    navigate('/')
                })
                
        })
    }
    return (
        <>
        <body style={{backgroundColor: '#f2f5f7',backgroundImage:'none',backgroundSize:'cover'}}> 
            {productLists.map((product, index) => {
                return <div key={index}>
                <div className='single-product-container-picked' style={{ marginBottom: '2%' }}>
                    <img src={product.image} alt='Product'></img>
                    <div className='product-top-name'>
                        <h5>{product.name}</h5>
                        <h6>Delivery price: {String(product.deliveryprice.toFixed(2)).replace(/\./g,",")}zł</h6>
                        <a href={product.link}>Link to the shop</a>
                    </div>
                    <div className='price-add-container'>    
                        <h3>{product.price}zł</h3>
                        <Form.Select className='select' onChange={handleChange}>
                                                        <option value="1">1</option>
                                                        <option value="2">2</option>
                                                        <option value="3">3</option>
                                                        <option value="5">5</option>
                                                        <option value="10">10</option>
                                                        <option value="20">20</option>
                                                </Form.Select>

                        <p >With ship {String((parseFloat(product.price.replace(/,/g, '.'))*parseFloat(selectedValue)+parseFloat(product.deliveryprice)).toFixed(2)).replace(/\./g,",")} zł</p>
                    </div>
                </div>
            </div>
            })}
            { !store.token ?
            <h5>Your product list</h5>
            :
            <button className='submit-btn' onClick={handleSubmit}>ZATWIERDŹ</button>

            }
            </body>
        </>
    )
}

export default SelectedProducts