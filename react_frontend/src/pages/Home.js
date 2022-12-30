import Navbar from "../components/Navbar";
import {useContext, useEffect} from "react";
import {Context} from "../store/appContext";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faMagnifyingGlass} from '@fortawesome/free-solid-svg-icons'
import ProductListModal from "../components/ProductListModal";
import LoginRegisterModal from "../components/LoginRegisterModal";
import '../css/Home.css'

function Home() {

    const {store, actions} = useContext(Context)

    useEffect(() => {
        actions.syncDataFromSessionStorage()
    }, [])

    return (
        <>
        <div className="title-container">
            <h1 >PRODUCTS <h1 className="title-2nd-part">APP</h1></h1>
            { !store.token ?
                <div className="login-container">
                    <LoginRegisterModal/>
                </div>
                :
                <div className="login-container">
                    <h1>{store.username}</h1>
                    <button onClick={() => actions.logout()}>Log out</button>
                </div>
            }        
        </div>
        <div className="search-bar-container">
            <h1>Najkorzystniejsze oferty dla Ciebie</h1>
            <div className="search-bar-inner-container">
            <FontAwesomeIcon className='icon' icon={faMagnifyingGlass}/>
                <form action="" >
                        <input type="text" placeholder="Type in product name"/>
                </form>
            </div>
            <button className="search-btn">Search</button>
            <ProductListModal/>
        </div>




        </>
    )
}

export default Home