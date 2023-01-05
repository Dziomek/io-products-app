import React, { useContext } from 'react'
import '../css/History.css'
import { useLocation } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { Context } from '../store/appContext'

const History = () => {
    
    const {store, actions} = useContext(Context)

    const location = useLocation()
    const navigate = useNavigate()

    const token = location.state && location.state.token

    console.log('History page rendered. Token: ', token)

    return (
        <div>
            History
        </div>
    )
}

export default History