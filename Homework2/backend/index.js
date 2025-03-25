const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
const port = 3001;

app.use(express.json());
app.use(cors());

// In-memory cache for aggregated results
const cache = {};
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes in milliseconds

// Function to clean expired cache entries
setInterval(() => {
    const now = Date.now();
    Object.keys(cache).forEach(key => {
      if (now - cache[key].timestamp >= CACHE_TTL) {
        delete cache[key];
      }
    });
}, 60 * 1000); // Runs every minute

app.get('/aggregate', async (req, res) => {
  const { book } = req.query;

  if (!book) {
    return res.status(400).json({ error: 'Missing query parameter: book is required' });
  }

  // Check cache first (case-insensitive key)
  const cacheKey = book.toLowerCase();
  if (cache[cacheKey]) {
    return res.status(200).json(cache[cacheKey].data);
  }

  let sw1Data = {}, sw2Data = {}, sw3Data = {};

  // --- SW1: Open Library API for book info ---
  try {
    const openLibraryUrl = `https://openlibrary.org/search.json?title=${encodeURIComponent(book)}`;
    const openLibraryResponse = await axios.get(openLibraryUrl);
    if (openLibraryResponse.data.docs && openLibraryResponse.data.docs.length > 0) {
      const firstResult = openLibraryResponse.data.docs[0];
      sw1Data = {
        title: firstResult.title,
        author_name: firstResult.author_name,
        first_publish_year: firstResult.first_publish_year,
        isbn: firstResult.isbn ? firstResult.isbn[0] : "N/A"
      };
    } else {
      sw1Data = { message: "No results found on Open Library API" };
    }
  } catch (err) {
    console.error('Error fetching SW1:', err.message);
    sw1Data = { error: 'Failed to fetch from Open Library API' };
  }

  // --- SW2: Wikipedia API for book summary ---
  try {
    const wikiUrl = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(book)}`;
    const wikiResponse = await axios.get(wikiUrl);
    sw2Data = wikiResponse.data;
  } catch (err) {
    console.error('Error fetching SW2:', err.message);
    sw2Data = { error: 'Failed to fetch from Wikipedia API' };
  }

  // --- SW3: Google Books API for additional metadata ---
  try {
    const googleBooksUrl = `https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(book)}`;
    const googleResponse = await axios.get(googleBooksUrl);
    if (googleResponse.data.totalItems > 0) {
      const volumeInfo = googleResponse.data.items[0].volumeInfo;
      sw3Data = {
        title: volumeInfo.title,
        authors: volumeInfo.authors,
        publisher: volumeInfo.publisher,
        publishedDate: volumeInfo.publishedDate,
        description: volumeInfo.description,
        pageCount: volumeInfo.pageCount,
        categories: volumeInfo.categories,
        imageLinks: volumeInfo.imageLinks
      };
    } else {
      sw3Data = { message: "No results found on Google Books API" };
    }
  } catch (err) {
    console.error('Error fetching SW3:', err.message);
    sw3Data = { error: 'Failed to fetch from Google Books API' };
  }

  const aggregatedResult = {
    sw1: sw1Data,
    sw2: sw2Data,
    sw3: sw3Data
  };

  // Cache the aggregated result
  cache[cacheKey] = { data: aggregatedResult, timestamp: Date.now() };

  res.status(200).json(aggregatedResult);
});

app.listen(port, () => {
  console.log(`Backend server listening on port ${port}`);
});