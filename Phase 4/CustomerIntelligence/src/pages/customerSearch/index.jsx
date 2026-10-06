import { useEffect, useState } from "react";
import axios from "axios";
import { BASE_URL } from "../../api";
import CustomerCard from "../../component/CustomerCard/customerCard";
import './index.css'

function CustomerSearch() {
  const [searchText, setSearchText] = useState("");
  const [record, setrecord] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  const getRecords = async () => {
      
    if (!searchText.trim()) {
      setError(false);
      return;
    }
      setLoading(true);
      setError(false);

      try {
        const response = await axios.get(
          `${BASE_URL}/customer/${searchText}`
        );

        console.log(response.data);
        setrecord(response.data);
      } catch (error) {
        console.error(error);
        setError(true);
      } finally {
        setLoading(false);
      }
    };

  return (
    <div>
      <strong>Search Customer BY id</strong>
      <hr/>
      <input
        type="text"
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
        placeholder="Search customer"
        className="search"
      />

      <button className="search-button" onClick={getRecords}>Search</button>

      {loading && <p>Loading...</p>}

      {!loading && error && (
        <p>Customer not found</p>
      )}

      {!loading && !error && 
        <CustomerCard 
          {...record}
        />
      }
    </div>
  );
}

export default CustomerSearch;