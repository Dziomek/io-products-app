import React, { useContext, useEffect } from 'react'
import '../css/History.css'
import { useLocation } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { Context } from '../store/appContext'

const History = () => {
    
    const {store, actions} = useContext(Context)

    const location = useLocation()
    const navigate = useNavigate()
    
    console.log('History page rendered. Token: ', store.token)

    useEffect(() => {
        actions.syncDataFromSessionStorage()
        if (!store.token) navigate('/')
    }, [])
    

    

    return (
        <div>
            { store.token ?
            <>
                {store.username} {store.email}
            </>
            :
            null
            }
        </div>
    )
}

export default History