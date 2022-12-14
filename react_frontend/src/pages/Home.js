import Navbar from "../components/Navbar";
import Progressbar from "../components/ProgressBar";
import ProductList from "../components/ProductList";
import {useContext, useEffect} from "react";
import {Context} from "../store/appContext";

function Home() {

    const {store, actions} = useContext(Context)

    useEffect(() => {
        actions.syncDataFromSessionStorage()
    }, [])

    return (
        <>
            <Navbar/>
            <ProductList/>
        </>
    )
}

export default Home