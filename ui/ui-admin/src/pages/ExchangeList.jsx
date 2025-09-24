import React, { useEffect, useState } from "react";
import { getExchanges, deleteExchange } from "../api/exchanges";

const ExchangeList = () => {
  const [exchanges, setExchanges] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setExchanges(await getExchanges());
  };

  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>API URL</th>
          <th>Active</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {exchanges.map((ex) => (
          <tr key={ex.exchange_id}>
            <td>{ex.exchange_id}</td>
            <td>{ex.name}</td>
            <td>{ex.api_url}</td>
            <td>{ex.is_active ? "Yes" : "No"}</td>
            <td>
              <button onClick={() => deleteExchange(ex.exchange_id).then(fetchData)}>
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ExchangeList;
