import React, {useState, useEffect} from "react";
import Navbar from "./components/Navbar";

function App() {
    const [data, setData] = useState([])

    useEffect(() => {
        fetch("http://127.0.0.1:5000").then(
            r => r.json()).then(
            data => {
            setData(data)
            console.log(data)
          })
    }, [])

    return (
    <div className="App">
      <Navbar/>
    </div>
  );
}

export default App;
