
import React, {useState, useRef, useEffect, useContext} from 'react'
import '../css/LoginRegisterModal.css'
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faPlus, faMinus, faXmark} from "@fortawesome/free-solid-svg-icons";
import Form from 'react-bootstrap/Form'
import DropdownButton from 'react-bootstrap/DropdownButton';
import DropdownItem from 'react-bootstrap/esm/DropdownItem';
import Dropdown from 'react-bootstrap/Dropdown';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';

const LoginRegisterModal = () => {
    
    const [show, setShow] = useState(false);
    const [activeButton, setActiveButton] = useState('login-button')

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    
    const switchActive = event => {
        setActiveButton(event.target.dataset.button)
    }

    return (
      <>
        <Button variant="primary" onClick={handleShow}>
            Login/register
        </Button>
  
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Login / registration</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <div className='login-register-navigation'>
                    <button data-button='login-button' 
                    className={activeButton === 'login-button' ? 'active' : ''} onClick={switchActive}>
                        SIGN IN
                    </button>
                    <button data-button='register-button'
                    className={activeButton === 'register-button' ? 'active' : ''} onClick={switchActive}>
                        CREATE AN ACCOUNT
                    </button>
                </div>
                <div className='login-register-form'>
                    {activeButton === 'login-button' ? 
                    <LoginForm/> 
                    : <RegisterForm/>}
                </div>
            </Modal.Body>
        </Modal>
      </>
    );
}

export default LoginRegisterModal