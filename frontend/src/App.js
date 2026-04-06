import { useState } from "react";
import axios from "axios";

export default function App() {
  const [login, setLogin] = useState({
    username: "",
    password: "",
  });

  const [form, setForm] = useState({
    source_branch: "",
    destination_branch: "",
    product: "",
    quantity: "",
  });

  const [token, setToken] = useState("");
  const [message, setMessage] = useState("");
  const [transferId, setTransferId] = useState("");
  const [summaryBranchId, setSummaryBranchId] = useState("");
  const [stocks, setStocks] = useState([]);

  const handleLoginChange = (e) => {
    setLogin({
      ...login,
      [e.target.name]: e.target.value,
    });
  };

  const handleFormChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const loginUser = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/token/",
        login
      );

      setToken(response.data.token);
      setMessage("Login successful");
    } catch (error) {
      setMessage("Username or password is wrong");
    }
  };

  const createTransfer = async () => {
    await axios.post(
      "http://127.0.0.1:8000/api/transfers/",
      form,
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );

    setMessage("Transfer created successfully");
  };

  const approveTransfer = async () => {
    await axios.post(
      `http://127.0.0.1:8000/api/transfers/${transferId}/approve/`,
      {},
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );

    setMessage("Transfer approved successfully");
  };

  const fetchSummary = async () => {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/branches/${summaryBranchId}/stock-summary/`,
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );

    setStocks(response.data);
    setMessage("Stock summary loaded");
  };

  return (
    <div style={{ maxWidth: "400px", margin: "50px auto" }}>
      <h2>Stock Transfer ERP</h2>

      <input
        name="username"
        placeholder="Username"
        onChange={handleLoginChange}
      />
      <br /><br />

      <input
        name="password"
        type="password"
        placeholder="Password"
        onChange={handleLoginChange}
      />
      <br /><br />

      <button onClick={loginUser}>Login</button>

      <hr />

      <input
        name="source_branch"
        placeholder="Source Branch ID"
        onChange={handleFormChange}
      />
      <br /><br />

      <input
        name="destination_branch"
        placeholder="Destination Branch ID"
        onChange={handleFormChange}
      />
      <br /><br />

      <input
        name="product"
        placeholder="Product ID"
        onChange={handleFormChange}
      />
      <br /><br />

      <input
        name="quantity"
        placeholder="Quantity"
        onChange={handleFormChange}
      />
      <br /><br />

      <button onClick={createTransfer}>Create Transfer</button>

      <hr />

      <input
        placeholder="Transfer ID"
        value={transferId}
        onChange={(e) => setTransferId(e.target.value)}
      />
      <br /><br />

      <button onClick={approveTransfer}>Approve Transfer</button>

      <hr />

      <input
        placeholder="Branch ID for Summary"
        value={summaryBranchId}
        onChange={(e) => setSummaryBranchId(e.target.value)}
      />
      <br /><br />

      <button onClick={fetchSummary}>Load Summary</button>

      {stocks.map((item, index) => (
        <p key={index}>
          {item.product_name} - {item.quantity}
        </p>
      ))}

      <p>{message}</p>
    </div>
  );
}