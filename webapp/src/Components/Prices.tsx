import React, { useState, useEffect } from 'react';
import './Prices.css';
import Apihost from '../Config';
import { ICryptoPrice, IPricesProps } from '../models/Price';

const url = `${Apihost}/prices`;

const Prices: React.FC<IPricesProps> = ({ cryptoPrices, onCryptoDataChange }) => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url);

        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }

        const data: ICryptoPrice[] = await response.json();
        console.log(data);
        onCryptoDataChange(data);
        setLoading(false);
      } catch (error) {
        console.error(error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <h2 className="coin-prices-header">Current Prices</h2>
      <div className="coin-prices-container">
        {loading ? (
          <p>Loading...</p>
        ) : (
          <ul className="coin-list">
            {cryptoPrices &&
              cryptoPrices.map((crypto) => (
                <li key={crypto.id} className="coin-list-item">
                  <span className="coin-name">{crypto.cryptocurrency}</span>
                  <span className="coin-price">${crypto.value}</span>
                </li>
              ))}
          </ul>
        )}
      </div>
    </>
  );
};

export default Prices;
