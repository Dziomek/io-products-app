import React from 'react'
import '../css/ConfirmEmailModal.css'


const ConfirmEmailModal = (props) => {
    return (
        <div className='confirm-email-container'>
            <div className='confirm-email-inner'>
                <span id='confirm-title'>Verify your email address</span>
            </div>
            <div className='confirm-email-inner'>
                <span id='confirm-subtitle'>We have sent an activation link to your e-mail address</span>
            </div>
            <div className='confirm-email-inner'>
                <span id='confirm-email'>{props.email}</span>
            </div>
        </div>
    )
}

export default ConfirmEmailModal