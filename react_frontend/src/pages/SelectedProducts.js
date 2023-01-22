import React, { useState, useEffect, useContext } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { Context } from '../store/appContext'

const SelectedProducts = () => {
    
    const {store, actions} = useContext(Context)
    const location = useLocation()
    const navigate = useNavigate()

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
        const options = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: store.id, 
                productLists: productLists
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
    }

    return (
        <>
            {productLists.map((product, index) => {
                return <div key={index}>
                <div className='single-product-container' style={{ marginBottom: '2%' }}>
                    <img src={product.image} alt='Product'></img>
                    <div className='product-top-name'>
                        <h5>{product.name}</h5>
                        <h6>Delivery price: {String(product.deliveryprice.toFixed(2)).replace(/\./g,",")}zł</h6>
                        <a href={product.link}>Link to the shop</a>
                    </div>
                    <div className='price-add-container'>    
                        <h3>{product.price}zł</h3>

                        <p>With ship {product.price + product.deliveryprice} zł</p>
                    </div>
                </div>
            </div>
            })}
            <button onClick={handleSubmit}>ZATWIERDŹ</button>
        </>
    )
}

export default SelectedProducts