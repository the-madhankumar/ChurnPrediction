import { useEffect, useState } from "react";
import axios from "axios";
import { BASE_URL } from "../../api";
import "./index.css";

function HighRiskCustomer() {
  const [records, setRecord] = useState([]);
  const [limit, setlimit] = useState(50);
  const [sortAscending, setSortAscending] = useState(true);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // #159 High Risk Fetch
  useEffect(() => {
    const getRecord = async () => {
      setLoading(true);
      setError("");

      try {
        const response = await axios.get(
          `${BASE_URL}/customers/high-risk?limit=${limit}`
        );

        setRecord(response.data.Records);
        console.log(response.data);
      } catch (error) {
        console.error(error);
        setError("Unable to load High Risk");
      } finally {
        setLoading(false);
      }
    };

    getRecord();
  }, [limit]);

  // #162 Load More
  const updateLimit = () => {
    setlimit((prev) => prev + 50);
  };

  // #163 Sort Toggle
  const toggleSort = () => {
    setSortAscending((prev) => !prev);
  };

  // #165 State Handling
  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (!records) {
    return null;
  }

  return (
    <center>
      {/* #161 Count Banner */}
      <h1>{records.length} high-risk customers identified</h1>

      {/* #162 Load More */}
      <button className="load-more" onClick={updateLimit}>
        Load More
      </button>

      {/* #163 Sort Toggle */}
      <button className="load-more" onClick={toggleSort}>
        Sort Tenure {sortAscending ? "^" : "v"}
      </button>

      {/* #160 Results Table */}
      {records.length === 0 ? (
        // #165 Empty Results
        <div>No high-risk customers found</div>
      ) : (
        [...records]
          .sort((a, b) =>
            sortAscending
              ? a.tenure - b.tenure
              : b.tenure - a.tenure
          )
          .map((item) => {
            const {
              contract_type,
              customer_id,
              monthly_charges,
              risk_reason,
              tenure
            } = item;

            return (
              <table
                className="high_risk_table"
                key={customer_id}
              >
                <tbody>
                  <tr>
                    <th>Customer ID</th>
                    <th>Tenure</th>
                    <th>Monthly Charges</th>
                    <th>Contract Type</th>
                    <th>Risk Reason</th>
                  </tr>

                  <tr>
                    <td>{customer_id}</td>
                    <td>{tenure}</td>
                    <td>
                      {/* #164 Currency Format */}
                      ${monthly_charges.toFixed(2)}
                    </td>
                    <td>{contract_type}</td>
                    <td>{risk_reason}</td>
                  </tr>
                </tbody>
              </table>
            );
          })
      )}
    </center>
  );
}

export default HighRiskCustomer;