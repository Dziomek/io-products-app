import React, { useContext, useEffect, useState } from 'react'
import '../css/History.css'
import { useLocation } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { Context } from '../store/appContext'
import { Link } from 'react-router-dom'
import LoginRegisterModal from '../components/LoginRegisterModal'

const History = () => {
    
    const {store, actions} = useContext(Context)
    const [historyData, setHistoryData] = useState(null)

    const location = useLocation()
    const navigate = useNavigate()
    
    console.log('History page rendered. Data: ', historyData)

    useEffect(() => {
        actions.syncDataFromSessionStorage()
        if (!store.token) {
            navigate('/')
            return
        }

        const options = {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: store.token ? store.id : ''
            })
        }
        console.log(options)
        
        fetch("http://10.160.73.81:5000/history", options)
            .then(res => {
                if (res.status === 200) return res.json()
            })
            .then(data => {
                if (data.history) setHistoryData(data.history)
                console.log(data.history, typeof historyData)
            })
            .catch(error => {
                console.log(error)
            })
    }, [])
    
    return (
        <>
        <body style={{backgroundColor:'#f2f5f7', backgroundImage:'none'}}>
        <div className="title-container">
            <Link style={{textDecoration: 'none'}} to='/'>
                <h1 >PRODUCTS <h1 className="title-2nd-part">APP</h1></h1>
            </Link>
            <div className="login-container">
                <h1></h1>
                <h1></h1>
                <h1>Hi {store.username}!</h1>
            </div>
        </div>
        <div className='history-container'>
            <div className='history-header' style={{padding: '2%'}}>
                <h1>Twoja historia produktów</h1>  
            </div>
            <div className='history-content'>
                    {historyData && historyData.map((item) => (
                        <div className='single-card' key={item.timestamp}>
                            <h2>Request made on: {item.timestamp}</h2>
                            {item.products.map((product) => (
                            <div key={product.name} className='grid-help'>                              
                                    <img src={product.image}></img>
                                    <h5>{product.name}</h5>
                                    <h5></h5>
                                    <h5>{product.price} zł</h5>
                                    <a></a>
                                    <a href={product.link}>View in shop</a>
                            </div>
                            ))}
                        </div>
                    ))}
            </div> 
        </div>
        </body>
        </>
    )
}

export default History