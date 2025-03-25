import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [bookTitle, setBookTitle] = useState('');
  const [aggregatedData, setAggregatedData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!bookTitle.trim()) {
      setError('Please enter a book title');
      return;
    }
    setLoading(true);
    try {
      setError('');
      setAggregatedData(null);
      const response = await axios.get('http://localhost:3001/aggregate', {
        params: { book: bookTitle }
      });
      setAggregatedData(response.data);
    } catch (err) {
      setError(err.response ? err.response.data.error : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Book Aggregator</h1>
      <div>
        <input
          type="text"
          placeholder="Enter Book Title"
          value={bookTitle}
          onChange={(e) => setBookTitle(e.target.value)}
          style={{ marginRight: '10px', width: '300px' }}
        />
        <button onClick={handleSearch}>Search</button>
      </div>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {aggregatedData && (
        <div style={{ marginTop: '20px' }}>
          <h2>Aggregated Results</h2>
          <div>
            <h3>SW1 (Open Library Book Info):</h3>
            <pre style={{ whiteSpace: 'pre-wrap' }}>
              {JSON.stringify(aggregatedData.sw1, null, 2)}
            </pre>
          </div>
          <div>
            <h3>SW2 (Wikipedia Summary):</h3>
            <pre style={{ whiteSpace: 'pre-wrap' }}>
              {JSON.stringify(aggregatedData.sw2, null, 2)}
            </pre>
          </div>
          <div>
            <h3>SW3 (Google Books Metadata):</h3>
            <pre style={{ whiteSpace: 'pre-wrap' }}>
              {JSON.stringify(aggregatedData.sw3, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;