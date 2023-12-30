import React, { useState } from 'react';

const App = () => {
  const [inputData, setInputData] = useState({
    userInput1: '',
    userInput2: '',
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
      <input
        type="text"
        name="userInput1"
        value={inputData.userInput1}
        onChange={handleInputChange}
      />
      <input
        type="text"
        name="userInput2"
        value={inputData.userInput2}
        onChange={handleInputChange}
      />
      {/* Add more input fields as needed */}
      <button onClick={handleSubmit}>Submit</button>
      <div>Backend Response: {backendResponse}</div>
    </div>
  );
};

export default App;
