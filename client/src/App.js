import React, { useState } from 'react';
import './App.css';
import logo from './ufclogo.png';
const App = () => {
  const [inputData, setInputData] = useState({
    userInput1: '',
    userInput2: '',
    odds : 0,
    // Add more input fields as needed
  });
  const [backendResponse, setBackendResponse] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async () => {
    //console.log('Button clicked');
    try {
      const response = await fetch('/members', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputData),
      });

      const data = await response.json();
      setBackendResponse(data.result);
      console.log('Backend Response:', data.result);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <div className="image-container">
      <img src={logo} alt="" />
      </div>


      <div className="space-between-divs"></div>

      <div>Enter two fighters to see the odds of who wins!</div>

      <div className="space-between-divs"></div>
      <input
        type="text"
        name="userInput1"
        placeholder='Red Fighter'
        value={inputData.userInput1}
        onChange={handleInputChange}
      />
      <input
        type="text"
        name="userInput2"
        placeholder='Blue Fighter'
        value={inputData.userInput2}
        onChange={handleInputChange}
      />
       <input
        type="text"
        name="odds"
        placeholder='Red fighter odds (optional)'
        value={inputData.odds}
        onChange={handleInputChange}
      />
      <button onClick={handleSubmit}>Submit</button>
      <div>{backendResponse}</div>
    </div>
  );
};

export default App;
