import { useEffect, useState } from "react";
import { fetchPrediction, fetchHistory } from "../api/client";

export function useDashboard() {
  const [selected, setSelected] = useState({
    year: "",
    month: "",
  });

  const [metrics, setMetrics] = useState({
    predicted_revenue: null,
    predicted_rides: null,
    predicted_top_category: null,
    loading: false,
  });

  const [history, setHistory] = useState([]);

  function setMonth(year, month) {
    if (!year || !month) return;

    setSelected({
      year: Number(year),
      month: Number(month),
    });
  }

  useEffect(() => {
    if (!selected.year || !selected.month) return;

    async function load() {
      setMetrics((m) => ({ ...m, loading: true }));

      // 🔹 cards
      const pred = await fetchPrediction(selected.year, selected.month);
      if (pred?.error) return;

      setMetrics({
        predicted_revenue: pred.predicted_revenue,
        predicted_rides: pred.predicted_rides,
        predicted_top_category: pred.predicted_top_category,
        loading: false,
      });

      // 🔹 chart (THIS WAS BROKEN)
      const seriesRes = await fetchHistory(selected.year, selected.month);

      // ✅ THIS LINE FIXES EVERYTHING
      setHistory(Array.isArray(seriesRes?.history) ? seriesRes.history : []);
    }

    load();
  }, [selected.year, selected.month]);

  return {
    selected,
    setMonth,
    metrics,
    history,
  };
}
