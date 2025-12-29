  import React from "react";
  import styles from "./MetricCard.module.css";
  import { formatCurrency, formatNumber } from "../../utils/formatters";

  export default function MetricCard({ label, value, loading = false, format = "number" }) {
    const displayed = loading ? "…" : format === "currency" ? formatCurrency(value) : format === "number" ? formatNumber(value) : (value ?? "-");
    return (
      <div className={styles.card}>
        <div className={styles.label}>{label}</div>
        <div className={styles.value}>{displayed}</div>
      </div>
    );
  }