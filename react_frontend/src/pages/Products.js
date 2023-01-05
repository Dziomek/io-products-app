import React from 'react'
import { useLocation } from 'react-router-dom'


const Products = () => {
    
    const location = useLocation()
    const productLists = location.state && location.state.productLists
    
    console.log('Products rendered. ProductsList: ', productLists)
    
    return (
        <div>
            { productLists ? 
            <>
            {
                productLists.map((object, index) => {
                    return <div key={index}>
                    <h1>{object.searchedProduct}</h1>
                    {object.productList.map((product, secondIndex) => {
                        return <div key={secondIndex} style={{marginBottom: '2%'}}>
                            <img src={product.image} alt='Product'></img>
                            <h4>{product.name}</h4>
                            <h5>{product.price}</h5>
                            
                            </div>
                    })}</div>
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