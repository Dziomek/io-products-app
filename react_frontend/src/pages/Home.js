import Navbar from "../components/Navbar";
import Progressbar from "../components/ProgressBar";
import ProductList from "../components/ProductList";
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