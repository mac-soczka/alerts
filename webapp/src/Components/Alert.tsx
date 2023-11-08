import React, { useState } from 'react';
import './Alert.css';
import Apihost from '../Config';
import { ICryptoPrice } from '../models/Price';
import { IAlert, IAlertProps } from '../models/Alert';

interface DateTimePickerProps {
  value: string;
  onChange: (value: string) => void;
}

interface DropdownProps {
  options: string[];
  selectedOption: string;
  onChange: (value: string) => void;
}


const url = `${Apihost}/alerts`;

const trigger_type: { [key: string]: string } = { "Value Change": "value_change", "Percent Change": "percent_change" };

const DateTimePicker: React.FC<DateTimePickerProps> = ({ value, onChange }) => (
  <input type="datetime-local" value={value} onChange={(e) => onChange(e.target.value)} />
);

const Dropdown: React.FC<DropdownProps> = ({ options, selectedOption, onChange }) => (
  <select value={selectedOption} onChange={(e) => onChange(e.target.value)}>
    {options.map((option) => (
      <option key={option} value={option}>
        {option}
      </option>
    ))}
  </select>
);

const Alert: React.FC<IAlertProps> = ({ cryptoPrices, onAlertUpdate, userId }) => {
  const [alert, setAlert] = useState({
    cryptocurrency: 'BTC',
    type: 'Value Change',
    value: '20',
    expiryDate: "2023-12-31T23:59",
    userId: userId
  });

  const handleInputChange = (field: string, value: string) => {
    setAlert((prevAlert) => ({
      ...prevAlert,
      [field]: value,
    }));
  };

  const handleSaveAlert = async () => {
    try {
      const currentPrice = cryptoPrices.find(data => data.cryptocurrency === alert.cryptocurrency)?.value || 0;
      const alertWithPrice = {
        cryptocurrency: alert.cryptocurrency,
        trigger_value: parseInt(alert.value, 10),
        trigger_type: trigger_type[alert.type],
        base_value: +currentPrice,
        user_id: userId,
        expires_at: alert.expiryDate
      };

      const response = await fetch(`${url}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(alertWithPrice),
      });

      const jsonResponse = await response.json();
      onAlertUpdate({ ...jsonResponse, expires_at: new Date(jsonResponse["expires_at"]).toUTCString() });

      console.log('Alert saved successfully');
      console.log('Response JSON:', jsonResponse);

      if (!response.ok) {
        throw new Error('Failed to save alert');
      }

      console.log('Alert saved successfully');
    } catch (error) {
      console.error('Error saving alert:', error);
    }
  };

  return (

    <>
      <h2>Add Alert</h2>
      <div className="alert-container">

        <div className="form-group">
          <label htmlFor="cryptocurrencyPicker">Select Cryptocurrency:</label>
          <Dropdown
            options={['BTC', 'ETH', 'TON']}
            selectedOption={alert.cryptocurrency}
            onChange={(value) => handleInputChange('cryptocurrency', value)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="typePicker">Select Type:</label>
          <Dropdown
            options={['Percent Change', 'Value Change']}
            selectedOption={alert.type}
            onChange={(value) => handleInputChange('type', value)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="value">Change {alert.type == "Percent Change" ? "in %" : "in $"}:</label>
          <input
            type="number"
            value={alert.value}
            onChange={(e) => handleInputChange('value', e.target.value)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="datetimePicker">Expiry Date:</label>
          <DateTimePicker
            value={alert.expiryDate}
            onChange={(value) => handleInputChange('expiryDate', value)}
          />
        </div>

        <button className="save-button" type="submit" onClick={handleSaveAlert}>
          Save Alert
        </button>
      </div>
    </>
  );
};

export default Alert;

