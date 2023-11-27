// OutputScreen.jsx
import React, { useState } from 'react';
import './OutputScreen.css'
import './SubmissionForm.css'
import axios from 'axios';

const OutputScreen = () => {
    const [action,setAction] = useState("Submit");
    const [paintingId, setPaintingId] = useState('');
    const [paintingData, setPaintingData] = useState(null);
    //const [error, setError] = useState('');

    const handleSearch = async () => {
        try {
            const response = await axios.get(`http://localhost:5000/search/${paintingId}`);
            
            setPaintingData(response.data);

        } catch (error) {
          console.error('Error fetching search results:', error);
        }
      };

    return(<div className="container">

        <div className="headerContainer"><div className="titleHeader">Wallace Collection, London </div></div>

        <div className="body">
        <div className="searchBar">
          <input
            type="text"
            placeholder="Search..."
            value={paintingId}
            onChange={(e) => setPaintingId(e.target.value)}
          />
          <button onClick={handleSearch}>Search</button>
          {
           paintingData && 
          (<div className="painting-info">
          <h2>Name: {paintingData.paintingName}</h2>
          <p>Year: {paintingData.year}</p>
        </div>
      )}
        </div>
        </div> 
    </div>); 
};

export default OutputScreen;