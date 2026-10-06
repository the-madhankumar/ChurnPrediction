import { useState } from "react";
import "./App.css";
import CustomerSearch from "./pages/customerSearch";
import ChurnSummary from "./pages/ChurnSummary";
import HighRiskCustomer from "./pages/HighRiskCustomer";
import ChurnPrediction from "./pages/ChurnPrediction";

function App() {
  const [activeTab, setActiveTab] = useState("home");

  return (
    <>
      <nav className="nav-bar">
        <button onClick={() => setActiveTab("home")}>
          Home
        </button>

        <button onClick={() => setActiveTab("customersearch")}>
          Customer Search
        </button>

        <button onClick={() => setActiveTab("churnsummary")}>
          Churn Summary
        </button>

        <button onClick={() => setActiveTab("highrisk")}>
          High Risk Customer
        </button>

        <button onClick={() => setActiveTab("churnpred")}>
          Churn Prediction
        </button>
      </nav>

      {activeTab === "home" && (
        <h1>Customer Intelligence Lab</h1>
      )}

      {activeTab === "customersearch" && (
        <CustomerSearch />
      )}

      {activeTab === "churnsummary" && (
        <ChurnSummary />
      )}

      {activeTab === "highrisk" && (
        <HighRiskCustomer />
      )}

      {activeTab === "churnpred" && (
        <ChurnPrediction />
      )}
    </>
  );
}

export default App;