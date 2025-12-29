// frontend/src/components/SummaryTable/SummaryTable.jsx
import React from "react";
import styles from "./SummaryTable.module.css";
import { formatCurrency, formatNumber } from "../../utils/formatters";

export default function SummaryTable({ rows = [], title = "Selected & Next Month (Overview)" }) {
  return (
    <div className={styles.card}>
      <div className={styles.header}>{title}</div>

      {(!rows || rows.length === 0) ? (
        <div className={styles.empty}>Select a month & year to see an overview.</div>
      ) : (
        <div className={styles.tableWrap}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Month</th>
                <th>Top Category</th>
                <th>Revenue</th>
                <th>Rides</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r, idx) => (
                <tr key={idx}>
                  <td className={styles.monthCell}>{r.month}</td>
                  <td>{r.top_category ?? "-"}</td>
                  <td>{typeof r.revenue === "number" ? formatCurrency(r.revenue) : (r.revenue ?? "-")}</td>
                  <td>{typeof r.rides === "number" ? formatNumber(r.rides) : (r.rides ?? "-")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
