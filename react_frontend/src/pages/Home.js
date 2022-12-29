import Navbar from "../components/Navbar";
import {useContext, useEffect} from "react";
import {Context} from "../store/appContext";
import ProductListModal from "../components/ProductListModal";

function Home() {

    const {store, actions} = useContext(Context)

    useEffect(() => {
        actions.syncDataFromSessionStorage()
    }, [])

    return (
        <>
            <Navbar/>
            <ProductListModal/>
        </>
    )
}

export default Home