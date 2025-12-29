import React, { useMemo } from "react";
import {
  ResponsiveContainer,
  LineChart as ReLineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
} from "recharts";
import { formatCurrency, formatNumber } from "../../utils/formatters";
import styles from "./LineChart.module.css";

export default function LineChart({ data = [] }) {
  const chartData = useMemo(() => {
    if (!Array.isArray(data)) return [];

    return data.map((d, idx) => {
      const name = d.label ?? d.month ?? d.name ?? `#${idx + 1}`;

      const rides =
        d.rides ?? d.predicted_rides ?? null;

      const revenue =
        d.revenue ?? d.predicted_revenue ?? null;

      return {
        name,
        rides: rides !== null ? Number(rides) : null,
        revenue: revenue !== null ? Number(revenue) : null,
      };
    });
  }, [data]);

  const hasRevenue = chartData.some((d) => typeof d.revenue === "number");
  const hasRides = chartData.some((d) => typeof d.rides === "number");

  if (!hasRevenue && !hasRides) {
    return <div className={styles.empty}>No chart data available.</div>;
  }

  return (
    <div className={styles.wrap}>
      <ResponsiveContainer width="100%" height={450}>
        <ReLineChart data={chartData}>
          <CartesianGrid stroke="#eef3f8" strokeDasharray="3 3" />
          <XAxis dataKey="name" />

          {hasRevenue && (
            <YAxis
              yAxisId="left"
              tickFormatter={formatCurrency}
              width={110}
            />
          )}

          {hasRides && (
            <YAxis
              yAxisId="right"
              orientation="right"
              tickFormatter={formatNumber}
              width={80}
            />
          )}

          <Tooltip />
          <Legend />

          {hasRevenue && (
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="revenue"
              stroke="#1f7a3a"
              strokeWidth={2}
              dot={{ r: 2 }}
            />
          )}

          {hasRides && (
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="rides"
              stroke="#2d6cff"
              strokeWidth={2}
              dot={{ r: 2 }}
            />
          )}
        </ReLineChart>
      </ResponsiveContainer>
    </div>
  );
}
