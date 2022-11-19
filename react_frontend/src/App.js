import React, {useState, useEffect} from "react";

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
      <h1>App</h1>
    </div>
  );
}

export default App;
