import React, { useContext, useEffect, useState } from 'react'
import '../css/History.css'
import { useLocation } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { Context } from '../store/appContext'

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
        
        fetch("http://127.0.0.1:5000/history", options)
            .then(res => {
                if (res.status === 200) return res.json()
            })
            .then(data => {
                setHistoryData(data)
                console.log(data)
            })
            .catch(error => {
                console.log(error)
            })
    }, [])
    
    return (
        <div>
            { store.token ?
            <>
                {store.username} {store.email} {store.id}
            </>
            :
            null
            }
        </div>
    )
}

export default History