import React, { useState, useEffect } from 'react';
import './AlertList.css';
import Apihost from '../Config';
import { IAlert, IAlertListProps } from "../models/Alert"

const url = `${Apihost}/alerts`;

const AlertList: React.FC<IAlertListProps> = ({ alerts, setAlerts, userId, cryptoPrices }) => {
  const [editingAlertId, setEditingAlertId] = useState<number | null>(null);
  const [editedAlert, setEditedAlert] = useState<Partial<IAlert>>({});
  const [loading, setLoading] = useState(true);

  const onEditAlert = (editedAlert: Partial<IAlert>) => {
    console.log('Edited Alert:', editedAlert);
  };

  useEffect(() => {
    const fetchData = async () => {
      console.log(`userId: ${userId}`)
      try {
        const response = await fetch(`${url}?userId=${userId}`, {
          method: 'GET',
        });
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }

        const data = await response.json();
        console.log(data);
        setAlerts(data);
        setLoading(false);
      } catch (error) {
        console.error(error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleDeleteClick = async (alertId: number) => {
    try {
      const response = await fetch(`${url}/${alertId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete alert');
      }

      setAlerts((prevAlerts) => prevAlerts.filter((alert) => alert.id !== alertId));
      console.log('Alert deleted successfully');
    } catch (error) {
      console.error('Error deleting alert:', error);
    }
  };

  const handleEditClick = (alertId: number) => {
    setEditingAlertId(alertId);
    setEditedAlert(alerts.find((alert) => alert.id === alertId) || {});
  };

  const handleCancelEdit = () => {
    setEditingAlertId(null);
    setEditedAlert({});
    console.log('Edit cancelled');
  };

  const handleSaveEdit = async () => {
    onEditAlert(editedAlert);
    setEditingAlertId(null);
    setEditedAlert({});
    setAlerts((prevAlerts) =>
      prevAlerts.map((alert) =>
        alert.id === editingAlertId
          ? { ...alert, ...editedAlert, expires_at: new Date(editedAlert.expires_at!).toUTCString() }
          : alert
      )
    );
    try {
      const currentPrice = +(cryptoPrices.find(data => data.cryptocurrency === editedAlert.cryptocurrency)?.value || 0);
      console.log("current price: ", currentPrice)
      const editedAlertConverted = {
        ...editedAlert,
        base_value: currentPrice,
        trigger_value: editedAlert.trigger_value !== undefined ? parseFloat(editedAlert.trigger_value.toString()) : 0,
        expires_at: convertToISODateTime(editedAlert.expires_at!),
      };

      const response = await fetch(`${url}/${editingAlertId}`, {
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editedAlertConverted),
        method: 'PUT',
      });

      if (!response.ok) {
        throw new Error('Failed to edit alert');
      }

      console.log('Alert edited successfully');
    } catch (error) {
      console.error('Error editing alert:', error);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setEditedAlert((prevEditedAlert) => ({
      ...prevEditedAlert,
      [field]: field === 'expires_at' ? convertToISODateTime(value) : value,
    }));
  };

  return (
    <div className="alert-list-container">
      <h2>Alerts List</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul className="alert-list">
          {alerts.map((alert) => (
            <li key={alert.id} className={editingAlertId === alert.id ? 'editing' : ''}>
              <div className="alert-details">
                {editingAlertId === alert.id ? (
                  <>
                    <p>
                      <strong>Cryptocurrency:</strong>
                      <select
                        value={editedAlert.cryptocurrency}
                        onChange={(e) => handleInputChange('cryptocurrency', e.target.value)}
                      >
                        <option value="BTC">BTC</option>
                        <option value="ETH">ETH</option>
                        <option value="TON">TON</option>
                      </select>
                    </p>
                    <p>
                      <strong>Type:</strong>
                      <select
                        value={editedAlert.trigger_type}
                        onChange={(e) => handleInputChange('trigger_type', e.target.value)}
                      >
                        <option value="percent_change">Percent Change</option>
                        <option value="value_change">Value Change</option>
                      </select>
                    </p>
                    <p>
                      <strong>Value:</strong>
                      <input
                        type="number"
                        value={editedAlert.trigger_value}
                        onChange={(e) => handleInputChange('trigger_value', e.target.value)}
                      />
                    </p>
                    <p>
                      <strong>Expiry Date:</strong>
                      <input
                        type="datetime-local"
                        value={convertToISODateTime(editedAlert.expires_at || '')}
                        onChange={(e) => handleInputChange('expires_at', e.target.value)}
                      />
                    </p>
                  </>
                ) : (
                  <>
                    <p>
                      <strong>Cryptocurrency: </strong> {alert.cryptocurrency}
                    </p>
                    <p>
                      <strong>Type: </strong> {alert.trigger_type}
                    </p>
                    <p>
                      <strong>Value: </strong>
                      {alert.trigger_type === 'value_change' ? `$${alert.trigger_value}` : alert.trigger_value}
                      {alert.trigger_type === 'percent_change' && '%'}
                    </p>
                    <p>
                      <strong>Expiry Date :</strong> {alert.expires_at}
                    </p>
                  </>
                )}
              </div>
              <div className="alert-actions">
                {editingAlertId === alert.id ? (
                  <>
                    <button onClick={handleCancelEdit}>Cancel</button>
                    <button onClick={handleSaveEdit}>Save</button>
                  </>
                ) : (
                  <div className="alert-actions-delete">
                    <button onClick={() => handleEditClick(alert.id)}>Edit</button>
                    <button className="btn-delete" onClick={() => handleDeleteClick(alert.id)}>
                      Delete
                    </button>
                  </div>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

const convertToISODateTime = (value: string) => {
  const dateObject = new Date(value);
  if (!isNaN(dateObject.getTime())) {
    const year = dateObject.getFullYear();
    const month = (dateObject.getMonth() + 1).toString().padStart(2, '0');
    const day = dateObject.getDate().toString().padStart(2, '0');
    const hours = dateObject.getHours().toString().padStart(2, '0');
    const minutes = dateObject.getMinutes().toString().padStart(2, '0');

    return `${year}-${month}-${day}T${hours}:${minutes}`;
  }
  return value;
};

export default AlertList;
