// src/pages/Dashboard.jsx
import React from "react";
import { useDashboard } from "../hooks/useDashboard";
import MetricCard from "../components/MetricCard/MetricCard";
import LineChart from "../components/LineChart/LineChart";
import SummaryTable from "../components/SummaryTable/SummaryTable";
import MonthSelector from "../components/MonthSelector/MonthSelector";

export default function Dashboard() {
  const { selected, setMonth, metrics, history, recentRows } = useDashboard();

  return (
    <div className="page-shell">
      <header className="page-header">
        <div className="page-title">RideSense – Predicting the Future of Mobility</div>
        <div className="page-sub">
          Your next ride? Already predicted. Your future? Already optimized.
        </div>
      </header>

      <main className="page-main">
        <div className="top-bar">
          <MonthSelector
            year={selected.year}
            month={selected.month}
            onChange={setMonth}
          />
        </div>

        <section className="cards-grid">
          <MetricCard label="Predicted Revenue" value={metrics.predicted_revenue} loading={metrics.loading} format="currency" />
          <MetricCard label="Predicted Rides" value={metrics.predicted_rides} loading={metrics.loading} format="number" />
          <MetricCard label="Top Category" value={metrics.predicted_top_category} loading={metrics.loading} format="text" />
        </section>

        <section className="chart-area">
          <LineChart data={history} />
        </section>
      </main>
    </div>
  );
}