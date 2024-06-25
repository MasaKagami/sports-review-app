// src/pages/Home.jsx
import React, { useEffect, useState } from 'react';
import apiClient from '../apiClient';

const Home = () => {
  const [games, setGames] = useState([]);

  useEffect(() => {
    apiClient.get('/games/')
      .then(response => {
        setGames(response.data);
      })
      .catch(error => {
        console.error('Error fetching games:', error);
      });
  }, []);

  return (
    <div>
      <h1>Upcoming Games</h1>
      <ul>
        {games.map(game => (
          <li key={game.id}>
            {game.title} - {new Date(game.date).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Home;
